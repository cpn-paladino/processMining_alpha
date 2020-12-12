import pkgutil
import logging
from enum import Enum

import util.xes_constants as xes_constants
import util.date.dummy as dt_parser
from objects.log.log import EventLog, Trace, Event
from util.generatelog import sorting, index_attribute
from util.generatelog import parameters as param_util
from util.Parameters import Parameters


# ITERPARSE EVENTS
_EVENT_END = 'end'
_EVENT_START = 'start'

# function to check is the element is Null
def checkElementIsNotNone(element):
    resultBool = False    
    if(element is not None):
        resultBool = True
    return resultBool

def addStringOnTree(tree, parent, element, log, event, trace):
    if checkElementIsNotNone(parent):
        tree = __parse_attribute(element, parent, \
               element.get(xes_constants.KEY_KEY), \
               element.get(xes_constants.KEY_VALUE), tree)

def addDateOnTree(tree, parent, element, log, event, trace):   
    date_parser = dt_parser            
    try:
        dt = date_parser.apply(element.get(xes_constants.KEY_VALUE))
        tree = __parse_attribute(element, parent, element.get(xes_constants.KEY_KEY), dt, tree)
    except TypeError:
        logging.info("failed to parse date: " + str(element.get(xes_constants.KEY_VALUE)))
    except ValueError:
        logging.info("failed to parse date: " + str(element.get(xes_constants.KEY_VALUE)))    

def addEventOnTree(tree, parent, element, log, event, trace):
	tree[element] = event

def addTraceOnTree(tree, parent, element, log, event, trace):
    tree[element] = trace.attributes	

def addFloatOnTree(tree, parent, element, log, event, trace):
	if checkElementIsNotNone(parent):
		try:
			val = float(element.get(xes_constants.KEY_VALUE))
			tree = __parse_attribute(element, parent, element.get(xes_constants.KEY_KEY), val, tree)
		except ValueError:
			logging.info("failed to parse float: " + str(element.get(xes_constants.KEY_VALUE)))	

def addIntOnTree(tree, parent, element, log, event, trace):            
	if checkElementIsNotNone(parent):
		try:
			val = int(element.get(xes_constants.KEY_VALUE))
			tree = __parse_attribute(element, parent, element.get(xes_constants.KEY_KEY), val, tree)
		except ValueError:
			logging.info("failed to parse int: " + str(element.get(xes_constants.KEY_VALUE)))			

def addBooleanOnTree(tree, parent, element, log, event, trace):
	if checkElementIsNotNone(parent):
		try:
			val0 = element.get(xes_constants.KEY_VALUE)
			val = False
			if str(val0).lower() == "true":
				val = True
			tree = __parse_attribute(element, parent, element.get(xes_constants.KEY_KEY), val, tree)
		except ValueError:
			logging.info("failed to parse boolean: " + str(element.get(xes_constants.KEY_VALUE)))

def addListOnTree(tree, parent, element, log, event, trace):
	if checkElementIsNotNone(parent):
		# lists have no value, hence we put None as a value
		tree = __parse_attribute(element, parent, element.get(xes_constants.KEY_KEY), None, tree)

def addIDOnTree(tree, parent, element, log, event, trace):
	if checkElementIsNotNone(parent):
		tree = __parse_attribute(element, parent, element.get(xes_constants.KEY_KEY),
								 element.get(xes_constants.KEY_VALUE), tree)

def addExtensionOnTree(tree, parent, element, log, event, trace):    
    if log is None:
        raise SyntaxError('extension found outside of <log> tag')
    if checkElementIsNotNone(element.get(xes_constants.KEY_NAME)) and \
        checkElementIsNotNone(element.get(xes_constants.KEY_PREFIX)) and \
        checkElementIsNotNone(element.get(xes_constants.KEY_URI)):
            log.extensions[element.get(xes_constants.KEY_NAME)] = {
                xes_constants.KEY_PREFIX: element.get(xes_constants.KEY_PREFIX),
                xes_constants.KEY_URI: element.get(xes_constants.KEY_URI)}

def addGlobalOnTree(tree, parent, element, log, event, trace):    
	if log is None:
		raise SyntaxError('global found outside of <log> tag')
	if checkElementIsNotNone(element.get(xes_constants.KEY_SCOPE)):
		log.omni_present[element.get(xes_constants.KEY_SCOPE)] = {}
		tree[element] = log.omni_present[element.get(xes_constants.KEY_SCOPE)]

def addClassifierOnTree(tree, parent, element, log, event, trace): 
	if log is None:
		raise SyntaxError('classifier found outside of <log> tag')
	if checkElementIsNotNone(element.get(xes_constants.KEY_KEYS)):
		classifier_value = element.get(xes_constants.KEY_KEYS)
		if "'" in classifier_value:
			log.classifiers[element.get(xes_constants.KEY_NAME)] = [x for x in classifier_value.split("'")
																 if x.strip()]
		else:
			log.classifiers[element.get(xes_constants.KEY_NAME)] = classifier_value.split()		

def addLogOnTree(tree, parent, element, log, event, trace):
    tree[element] = log.attributes

actionsAddElementType = {
    xes_constants.TAG_STRING: addStringOnTree,
    xes_constants.TAG_DATE: addDateOnTree,
    xes_constants.TAG_EVENT: addEventOnTree,
    xes_constants.TAG_TRACE: addTraceOnTree,
    xes_constants.TAG_FLOAT: addFloatOnTree,
    xes_constants.TAG_INT: addIntOnTree,
    xes_constants.TAG_BOOLEAN: addBooleanOnTree,
    xes_constants.TAG_LIST: addListOnTree,        
    xes_constants.TAG_ID: addIDOnTree, 
    xes_constants.TAG_EXTENSION: addExtensionOnTree, 
    xes_constants.TAG_GLOBAL: addGlobalOnTree, 
    xes_constants.TAG_CLASSIFIER: addClassifierOnTree,
    xes_constants.TAG_LOG: addLogOnTree,
}

# 1 import method from file, removed parameters
def import_log(filename):
    
    """
    Imports an XES file into a log object

    Parameters
    ----------
    filename:
        Absolute filename
    parameters
        Parameters of the algorithm, including
            Parameters.TIMESTAMP_SORT -> Specify if we should sort log by timestamp
            Parameters.TIMESTAMP_KEY -> If sort is enabled, then sort the log by using this key
            Parameters.REVERSE_SORT -> Specify in which direction the log should be sorted
            Parameters.INSERT_TRACE_INDICES -> Specify if trace indexes should be added as event attribute for each event
            Parameters.MAX_TRACES -> Specify the maximum number of traces to import from the log (read in order in the XML file)
    Returns
    -------
    log : :class:`log.log.EventLog`
        A log
    """
    from lxml import etree    
    # 3 created a empty dictionary of parameters
    parameters = dict()
    
    # 3 Pass a parameter INSERT_TRACE_INDICES: Specify if trace indexes should be added as event attribute for each event   
    # INSERT_TRACE_INDICES = False -> Because they aren't added
    insert_trace_indexes = Parameters.INSERT_TRACE_INDICES
    
    # 5 Pass a VALUE of parameter INSERT_TRACE_INDICES    
    # Parameters.MAX_TRACES.value = 1.000.000.000 one bilion -> the max number of traces
    max_no_traces_to_import = Parameters.MAX_TRACES

    # 6 Return a method called "apply" to convert data
    date_parser = dt_parser

    # 7 convert xml to Tree of Elements according event at xml using SAX style parsing
    context = etree.iterparse(filename, events=[_EVENT_START, _EVENT_END])


    ''' 
     check to see if log has a namespace before looking for traces  (but this might be more effort than worth)
     but you could just assume that log use on the standard namespace desbried in XES
     to only find elements that start a trace use tag="{http://www.xes-standard.org}trace"
     or just use the {*} syntax to match to all namespaces with a trace element
    '''
    # 8 count number of traces and setup progress bar
    no_trace = sum([1 for trace in etree.iterparse(filename, events=[_EVENT_START], tag="{*}trace")])

    # 9 make tqdm facultative
    progress = None
    if pkgutil.find_loader("tqdm"):
        from tqdm.auto import tqdm
        progress = tqdm(total=no_trace, desc="parsing log, completed traces :: ")
    
    # 10 initialize objects: log, trace and event
    log = None
    trace = None
    event = None

    # 11 create a tree structure
    tree = {}

    # 12 iterate a context xml elements structure
    for tree_event, elem in context:
        
        # 13 check element is a start event
        if tree_event == _EVENT_START:  
            # 14 get parent of Node
            parent = tree[elem.getparent()] if elem.getparent() in tree else None
            # get type of element
            # print(elem.tag)
            # 15 get type of node according to actionsAddElementType
            keyAction = elem.tag.strip()    
            # 16 check if type element is at actionsAddElementType         
            if (keyAction in actionsAddElementType):
                # special case, it's needed create this structure
                if (keyAction == xes_constants.TAG_EVENT):
                    if checkElementIsNotNone(event):
                        raise SyntaxError('file contains <event> in another <event> tag')                                
                    event = Event() 
                # special case, it's needed create this structure
                elif (keyAction == xes_constants.TAG_TRACE):                    
                    if len(log) >= max_no_traces_to_import:
                        break
                    if checkElementIsNotNone(trace):
                        raise SyntaxError('file contains <trace> in another <trace> tag')
                    trace = Trace()   
                # special case, it's needed create this structure
                elif (keyAction == xes_constants.TAG_LOG):                    
                    if checkElementIsNotNone(log):
                        raise SyntaxError('file contains > 1 <log> tags')
                    log = EventLog()                    
                # just run action (function)    
                actionsAddElementType[keyAction](tree, parent, elem, log, event, trace)                
                continue
        elif tree_event == _EVENT_END:
            if elem in tree:
                del tree[elem]
            elem.clear()
            if checkElementIsNotNone(elem.getprevious()):
                try:
                    del elem.getparent()[0]
                except TypeError:
                    pass
            if elem.tag.endswith(xes_constants.TAG_EVENT):
                if checkElementIsNotNone(trace):
                    trace.append(event)
                    event = None
                continue

            elif elem.tag.endswith(xes_constants.TAG_TRACE):
                # TESTE ELIO
                if checkElementIsNotNone(log):
                    log.append(trace)
                # update progress bar as we have a completed trace
                if checkElementIsNotNone(progress):
                    progress.update()

                trace = None
                continue
            elif elem.tag.endswith(xes_constants.TAG_LOG):
                continue

    # gracefully close progress bar
    if checkElementIsNotNone(progress):
        progress.close()
    del context, progress

    if Parameters.TIMESTAMP_SORT in parameters and parameters[Parameters.TIMESTAMP_SORT]:
        log = sorting.sort_timestamp(log,
                                     timestamp_key=param_util.fetch(Parameters.TIMESTAMP_KEY, parameters),
                                     reverse_sort=param_util.fetch(Parameters.REVERSE_SORT, parameters))
    if insert_trace_indexes:
        log = index_attribute.insert_event_index_as_event_attribute(log)

    return log

def __parse_attribute(elem, store, key, value, tree):
    if len(elem.getchildren()) == 0:
        if type(store) is list:
            # changes to the store of lists: not dictionaries anymore
            # but pairs of key-values.
            store.append((key, value))
        else:
            store[key] = value
    else:
        if elem.getchildren()[0].tag.endswith(xes_constants.TAG_VALUES):
            store[key] = {xes_constants.KEY_VALUE: value, xes_constants.KEY_CHILDREN: list()}
            tree[elem] = store[key][xes_constants.KEY_CHILDREN]
            tree[elem.getchildren()[0]] = tree[elem]
        else:
            store[key] = {xes_constants.KEY_VALUE: value, xes_constants.KEY_CHILDREN: dict()}
            tree[elem] = store[key][xes_constants.KEY_CHILDREN]
    return tree
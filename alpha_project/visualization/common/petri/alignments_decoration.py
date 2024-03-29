from util.colors import get_transitions_color


def get_alignments_decoration(net, im, fm, log=None, aligned_traces=None, parameters=None):
    """
    Get a decoration for the Petri net based on alignments

    Parameters
    -------------
    net
        Petri net
    im
        Initial marking
    fm
        Final marking
    log
        Event log
    aligned_traces
        Aligned traces
    parameters
        Parameters of the algorithm

    Returns
    -------------
    decorations
        Decorations to use
    """
    if parameters is None:
        parameters = {}
    if aligned_traces is None and log is not None:
        
        aligned_traces = alignments.apply(log, net, im, fm, parameters={"ret_tuple_as_trans_desc": True})
    decorations = {}
    net_transitions = {}
    for trans in net.transitions:
        net_transitions[trans.name] = trans
    for align_trace0 in aligned_traces:
        align_trace = align_trace0["alignment"]
        for move in align_trace:
            move_trans_name = move[0][1]
            activity_trace_name = move[0][0]
            if move_trans_name in net_transitions:
                trans = net_transitions[move_trans_name]
                if trans not in decorations:
                    decorations[trans] = {"count_fit": 0, "count_move_on_model": 0}

                if activity_trace_name == ">>":
                    decorations[trans]["count_move_on_model"] = decorations[trans]["count_move_on_model"] + 1
                else:
                    decorations[trans]["count_fit"] = decorations[trans]["count_fit"] + 1

    for trans in decorations:
        if trans.label is not None:
            decorations[trans]["label"] = trans.label + " (" + str(
                decorations[trans]["count_move_on_model"]) + "," + str(decorations[trans]["count_fit"]) + ")"
            decorations[trans]["color"] = get_transitions_color(decorations[trans]["count_move_on_model"],
                                                                decorations[trans]["count_fit"])

    return decorations

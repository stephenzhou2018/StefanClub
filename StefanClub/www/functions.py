

def analysis_specify_filter(specify_filter):
    and_index = -1
    first_spe_filter = ''
    second_spe_filter = ''
    if len(specify_filter) > 0:
        if 'and' in specify_filter:
            and_index = specify_filter.index('and')
            first_spe_filter = specify_filter[:and_index]
            second_spe_filter = specify_filter[and_index + 3:]
        else:
            first_spe_filter = specify_filter
    else:
        pass
    return first_spe_filter, second_spe_filter

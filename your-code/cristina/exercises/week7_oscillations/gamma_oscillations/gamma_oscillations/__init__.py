

def merge_dicts(list_of_dicts):
    z = list_of_dicts[0].copy()   # start with x's keys and values
    for d in list_of_dicts[1:]:
        z.update(d)    # modifies z with y's keys and values & returns None
    return z
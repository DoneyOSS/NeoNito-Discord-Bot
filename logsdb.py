from tinydb import Query, TinyDB

db = TinyDB('logger.json')
log = Query()

def logs(serId: int, logs_list=None, logs_text=None, user_text_log=None, warnings=0):
    logCheck = db.get(log.id == serId)

    if not logCheck:
        # db shit
        dataStructure = {
            'id': serId,
            'warnings': warnings,
            'logs': logs_list if logs_list is not None else [],
            'logs_text': [logs_text] if logs_text is not None else [],
            'user_text_log': [user_text_log] if user_text_log is not None else []
        }

        db.insert(dataStructure)
        return dataStructure

    # old servers logic thingy
    update = {}
    if logs_list is not None:
        update['logs'] = logs_list
    if warnings is not None:
        update['warnings'] = warnings
    if logs_text is not None and user_text_log is not None:
        msgs = logCheck.get('logs_text', [])
        niggasWhoDeleted = logCheck.get('user_text_log', [])
        msgs.append(logs_text)
        niggasWhoDeleted.append(user_text_log)
        update['logs_text'] = msgs
        update['user_text_log'] = niggasWhoDeleted
    
    if update:
        db.update(update, log.id == serId)
        logCheck = db.get(log.id == serId)
        
    return logCheck
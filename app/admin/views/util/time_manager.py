class TimeManager:
    column_default_sort = [('modified', True), ('created_at', True)]
    form_excluded_columns = ('deleted_at', 'created_at', 'modified_at')

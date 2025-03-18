from setting.models import DataSource

def get_datasource():
    datasource = DataSource.objects.first()
    return datasource.value

def is_google_sheet():
    datasource = get_datasource()
    return datasource == 'google_sheet'
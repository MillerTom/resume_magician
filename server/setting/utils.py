from setting.models import DataSource

def get_datasource():
    datasource = DataSource.objects.first()
    if not datasource:
        datasource = DataSource(value='google_sheet')
        datasource.save()
    return datasource.value

def is_google_sheet():
    datasource = get_datasource()
    return datasource == 'google_sheet'
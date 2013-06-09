import requests


class DotDict(dict):
    def __getattr__(self, attr):
        return self.get(attr, None)
    
    __setattr__= dict.__setitem__
    __delattr__= dict.__delitem__


class EntityClient(object):
    PLURAL_TO_SINGULAR = {'companies': 'company',
                          'people': 'person',
                          'financial-organizations': 'financial-organization',
                          'products': 'product',
                          'service-providers': 'service-provider'}
    
    def __init__(self, type, api_key):
        self.type = type
        self.key = api_key
        self.base_url = 'http://api.crunchbase.com/v/1'
        
    def format(self, response, format):
        if format == 'json':
            return response.json(object_hook=DotDict)
        elif format == 'text':
            return response.text
        elif format == 'response':
            return response
        
    def get_by_name(self, name, format='json'):
        url = '{base_url}/{entity_type}/{name}.js?api_key={api_key}'.format(
            base_url=self.base_url,
            entity_type=self.PLURAL_TO_SINGULAR[self.type],
            name=name,
            api_key=self.key)
        
        return self.format(requests.get(url), format)
    
    def get_all(self, format='json'):
        url = '{base_url}/{entity_type}.js?api_key={api_key}'.format(
            base_url=self.base_url,
            entity_type=self.type,
            api_key=self.key)
        
        return self.format(requests.get(url), format)
    

class CrunchBaseClient(object):
    def __init__(self, api_key):       
        self.companies                  = EntityClient('companies', api_key)
        self.people                     = EntityClient('people', api_key)
        self.financial_organizations    = EntityClient('financial-organizations', api_key)
        self.products                   = EntityClient('products', api_key)
        self.service_providers          = EntityClient('service-providers', api_key)
    
    def __setattr__(self,attr,value):
        if attr =="__cardID":
            raise AttributeError('Attribute CardID is read only.')

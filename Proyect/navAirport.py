class NavAirport: 
    def __init__ (self, name, sids=None, stars=None): 
        self.name = name 
        self.sids = sids if sids is not None else []
        self.stars = stars if stars is not None else []

    def __str__ (self): 
        return f"{self.name} - SIDs: {self.sids} | STARs: {self.stars}"
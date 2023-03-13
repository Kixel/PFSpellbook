class Spell:
    
    schools = [""]
    descriptors = [""]
    
    def __init__(self) -> None:
        self.SR = False
        self.save = ""
        self.duration = ""
        self.range = ""
        self.target = ""
        self.description = ""
        self.casttime = ""
        self.vocal = False
        self.somatic = False
        self.source = []
        self.sourcebook = []
        self.cheapmaterial = False
        self.focus = False
        self.divinefocus = False
        self.dismissable = False
        self.expensivematerial = False
        self.school = ""
        self.subschool = ""
        self.descriptors = []
        self.url = ""
        self.pfslegal = False
        self.pfsrestricted = False
        self.threefive = False
        self.name = ""
        self.levels = []
        
    def validateSpell(self) -> bool:
        if self.save == "" or self.duration == "" or self.range == "" or self.target == "" or self.description == "" or self.casttime == "" or len(self.source) == 0 or len(self.sourcebook) == 0 or self.school == "" or self.url == "" or self.url == "" or (self.pfslegal and not self.pfsrestricted) or len(self.levels) == 0:
            return False
        return True
        
        
    def save(self, filename : str) -> bool:
        pass

    def load(self, filename : str) -> bool:
        pass
        
    #def __repr__(self) -> str:
    #    pass
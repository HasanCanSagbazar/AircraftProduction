from django.db import models

class UavsAssemblyManager(models.Manager):
    
    def all_assemblies(self):
        """Return all assemblies"""
        return self.all()
    

class AssemblyPartManager(models.Manager):
    
    def all_used_parts(self):
        """Return all parts"""
        return self.all()
def splitthousands(s, sep=','):  
    if len(s) <= 3:  
        return s  
    return splitthousands(s[:-3], sep) + sep + s[-3:]  

print splitthousands('45168313818651')
print splitthousands('45168313818651', '.')

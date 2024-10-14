
class RelationshipFinder:

    def findUsecaseRelationship(doc, actors):
        relationship = []
        for i,token in enumerate(doc):
            if token.pos_ == 'VERB':
                for child in token.children:
                    if child.pos_ == 'NOUN':
                        for actor in actors:
                            if actor == child.text:
                                dobj = ''
                                for grandchild in token.children:
                                    if grandchild.dep_ == 'dobj':
                                        dobj = grandchild.text
                                if i+2 < len(doc) - 1 and (doc[i+1].text.lower() == 'and' or doc[i+1].text.lower() == 'or'):
                                    for grandchild in doc[i+2].children:
                                        if grandchild.dep_ == 'dobj':
                                            dobj = grandchild.text
                                            relationship.append(f"{child.text} --> \"{doc[i+2].text} {dobj}\"")
                                if dobj:
                                    relationship.append(f"{child.text} --> \"{token.text} {dobj}\"")
                                else:
                                    relationship.append(f"{child.text} --> \"{token.text}\"")
        return relationship
    

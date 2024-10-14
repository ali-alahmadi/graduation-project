import os
import plantuml
import time


class GenerateDiagram():
    def GenerateUsecase(cleanResults):
        with open('umlfile/usecase.uml', 'w') as f:
            f.write("@startuml\n \n")
            for actor in cleanResults['actors']:
                f.write(f"actor {actor}\n")
            f.write("rectangle {\n")
            for usecase in cleanResults['usecases']:
                f.write(f"usecase \"{usecase}\" \n")
            for ucr in cleanResults['usecase relationship']:
                f.write(f"{ucr}\n")
            f.write("} \n")
            f.write("\n@enduml \n")
        
    def GenerateClassDiagram(cleanResults, results, texts):
        classes = {}
        with open('umlfile/class.uml', 'w') as f:
            f.write("@startuml\n\n'Classes:\n'-------------\n\n")
            for clas in cleanResults['class']:
                for text in texts:
                    for clasresulte in results[text]['class']:
                        clasresulte_without_quotes = clasresulte.strip("'")
                        if clas == clasresulte_without_quotes:
                            if clas not in classes:
                                classes[clas] = {'attributes': [], 'method': []}
                            if results[text].get('attributes'):
                                classes[clas]['attributes'].extend(results[text]['attributes'])
                            if results[text].get('method'):
                                classes[clas]['method'].extend(results[text]['method'])

                attributes = classes.get(clas, {}).get('attributes', [])
                attributes = list(set(attributes))
                classes[clas]['attributes'] = attributes  

                method = classes.get(clas, {}).get('method', [])
                method = list(set(method))
                classes[clas]['method'] = method 

                f.write(f"class {clas} ""{\n")
                if classes.get(clas, {}).get('attributes'):
                    for attribute in classes.get(clas, {}).get('attributes'):
                        f.write(f"  - {attribute}: String\n")
                if classes.get(clas, {}).get('method'):
                    for method in classes.get(clas, {}).get('method'):
                        f.write(f"  + {method}\n")
                f.write("} \n\n")
            f.write("'Associations:\n'-------------\n\n")
            f.write("\n@enduml \n")


    def generate_image(diagram_type):
        if diagram_type == 'class':
            uml_file_path = "umlfile/class.uml"
            image_path = "class.svg"
            save_path = "static/diagram/class.svg"
            plantuml_instance = plantuml.PlantUML(url='http://www.plantuml.com/plantuml/svg/')
            plantuml_instance.processes_file(uml_file_path, outfile=save_path)
            return image_path
        elif diagram_type == 'usecase':
            uml_file_path = "umlfile/usecase.uml"
            image_path = "usecase.svg"
            save_path = "static/diagram/usecase.svg"
            plantuml_instance = plantuml.PlantUML(url='http://www.plantuml.com/plantuml/svg/')
            plantuml_instance.processes_file(uml_file_path, outfile=save_path)
            while not os.path.exists(save_path):
                time.sleep(1)
            return image_path
        

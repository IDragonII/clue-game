from z3 import *

colonel_mustard = Bool("colonel_mustard")  # Coronel Mustard es el culpable.
miss_scarlet = Bool("miss_scarlet")         # Miss Scarlet es la culpable.
professor_plum = Bool("professor_plum")     # Profesor Plum es el culpable.
mrs_peacock = Bool("mrs_peacock")           # Mrs. Peacock es la culpable.
reverend_green = Bool("reverend_green")     # Reverend Green es el culpable.
mrs_white = Bool("mrs_white")               # Mrs. White es la culpable.

kitchen = Bool("kitchen")                    # El crimen ocurrió en la Cocina.
dining_room = Bool("dining_room")            # El crimen ocurrió en el Comedor.
living_room = Bool("living_room")            # El crimen ocurrió en la Sala.
library = Bool("library")                    # El crimen ocurrió en la Biblioteca.
study = Bool("study")                        # El crimen ocurrió en el Estudio.
garden = Bool("garden")                      # El crimen ocurrió en el Jardín.

knife = Bool("knife")                        # Se utilizó el cuchillo.
revolver = Bool("revolver")                  # Se utilizó el revólver.
rope = Bool("rope")                          # Se utilizó la cuerda.
poison = Bool("poison")                      # Se utilizó el veneno.
candlestick = Bool("candlestick")            # Se utilizó el candelabro.

knowledge = And(
    Not(living_room),            # El crimen NO ocurrió en la Sala.
    Not(library),                # El crimen NO ocurrió en la Biblioteca.
    Not(study),                  # El crimen NO ocurrió en el Estudio.
    Not(garden),                 # El crimen NO ocurrió en el Jardín.
    
    Or(kitchen, dining_room),    # El crimen ocurrió en la Cocina o en el Comedor.
    
    Not(revolver),               # El revólver NO fue usado.
    Implies(knife, Not(kitchen)),     # Si se usó el cuchillo, el crimen fue en la Cocina.
    Implies(candlestick, dining_room),  # Si se usó el candelabro, el crimen fue en el Comedor.
    
    Implies(professor_plum, Not(kitchen)),   # Si el Profesor Plum es el culpable, NO fue en la Cocina.
    Implies(miss_scarlet, dining_room),      # Si Miss Scarlet es la culpable, el crimen fue en el Comedor.

    Implies(mrs_white, Not(candlestick)),    # Si Mrs. White es culpable, no se usó el candelabro.
    Implies(colonel_mustard, knife),         # Si el Coronel Mustard es culpable, se usó el cuchillo.
    
    Or(knife, poison, candlestick),  # El crimen se cometió con el cuchillo, veneno o candelabro.
    Not(rope),                       # La cuerda NO fue usada.
    
    Implies(dining_room, knife),     # Si el crimen fue en el comedor, no se usó el cuchillo.
    Implies(kitchen, Not(candlestick)),   # Si el crimen fue en la cocina, no se usó el candelabro.
    
    Implies(Not(miss_scarlet), mrs_peacock),  # Si no fue Miss Scarlet, entonces fue Mrs. Peacock.
    Not(mrs_peacock)                          # Mrs. Peacock no fue la culpable.
)

def check_accusation(knowledge, query):
    s = Solver()
    s.add(knowledge)
    s.add(Not(query))
    if s.check() == unsat:
        return True
    else:
        return False
print("¿Es Miss Scarlet el culpable?", check_accusation(knowledge, miss_scarlet))
print("¿Es Professor Plum el culpable?", check_accusation(knowledge, professor_plum))
print("¿Es Mrs Peacock el culpable?", check_accusation(knowledge, mrs_peacock))
print("¿Es Reverend Green el culpable?", check_accusation(knowledge, reverend_green))
print("¿Es Colonel Mustard el culpable?", check_accusation(knowledge, colonel_mustard))
print("¿Es Mrs White el culpable?", check_accusation(knowledge, mrs_white))

print("¿Fue en la Cocina?", check_accusation(knowledge, kitchen))
print("¿Fue en el Comedor?", check_accusation(knowledge, dining_room))
print("¿Se usó el Cuchillo?", check_accusation(knowledge, knife))
print("¿Se usó el Revolver?", check_accusation(knowledge, revolver))
print("¿Se usó la Cuerda?", check_accusation(knowledge, rope))
print("¿Se usó el Veneno?", check_accusation(knowledge, poison))
print("¿Se usó el Candelabro?", check_accusation(knowledge, candlestick))
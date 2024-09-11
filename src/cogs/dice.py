import random

def roll_dice(num_rolls, sides, modifier_flag):
    rolls = []
    if modifier_flag == 1:
        # Exemplo: Todas as rolagens serão 1
        rolls = [1 for _ in range(num_rolls)]
    elif modifier_flag == 2:
        # Exemplo: Rolagens variam de 1 a metade dos lados
        rolls = [random.randint(1, sides // 2) for _ in range(num_rolls)]
    elif modifier_flag == 3:
        # Exemplo: Rolagens variam de metade + 1 até o número máximo de lados
        rolls = [random.randint((sides // 2) + 1, sides) for _ in range(num_rolls)]
    elif modifier_flag == 4:
        # Exemplo: Todas as rolagens serão o número máximo de lados
        rolls = [sides for _ in range(num_rolls)]
    elif modifier_flag == 5:
        # Exemplo: Seleção de valores específicos
        specific_numbers = [2, 4, 7, 8]
        rolls = [random.choice(specific_numbers) for _ in range(num_rolls)]
    else:
        # Sem modificador, rola normalmente
        rolls = [random.randint(1, sides) for _ in range(num_rolls)]

    return rolls

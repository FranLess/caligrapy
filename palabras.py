from enum import Enum


# TODO hacer vocabulario ruso basico en enum


class CursoRuso:
    class Lesion1(Enum):
        Человек = 1
        """persona"""
        мужчина = 2
        """hombre"""
        женщины = 3
        "mujer"
        парень = 4
        """joven/chico (hombre)"""
        девушка = 5
        """joven/chica (mujer)"""
        мальчик = 6
        """chico/niño"""
        девочка = 7
        """chica/niña"""
        дети = 8
        """niños"""
        



class Abecedario:
    class Ruso(Enum):
        а = 1
        б = 2
        в = 3
        г = 4
        д = 5
        е = 6
        ё = 7
        ж = 8
        з = 9
        и = 10
        й = 11
        к = 12
        л = 13
        м = 14
        н = 15
        о = 16
        п = 17
        р = 18
        с = 19
        т = 20
        у = 21
        ф = 22
        х = 23
        ц = 24
        ч = 25
        ш = 26
        щ = 27
        ъ = 28
        ы = 29
        ь = 30
        э = 31
        ю = 32
        я = 33

    class Español(Enum):
        a = 1
        b = 2
        c = 3
        d = 4
        e = 5
        f = 6
        g = 7
        h = 8
        i = 9
        j = 10
        k = 11
        l = 12
        m = 13
        n = 14
        ñ = 15
        o = 16
        p = 17
        q = 18
        r = 19
        s = 20
        t = 21
        u = 22
        v = 23
        w = 24
        x = 25
        y = 26
        z = 27


class Palabras:
    class Ruso:
        class Глаголы(Enum):
            """Verbos"""
            бежа́ть = 1
            """correr (sinónimo побежа́ть)"""
            побежа́ть = 2
            """correr (sinónimo бежа́ть)"""

        class Существительные(Enum):
            """Sustantivos"""
            философия = 1
            """filosofía"""
            привет = 2
            """hola"""
            Яблоко = 3
            """manzana"""
            человек = 4
            """persona"""
            женщины = 5
            """mujeres, las mujeres, unas mujeres"""
            мужчины = 6
            """hombres, del hombre, los hombres"""
            хлеб = 7
            """pan"""

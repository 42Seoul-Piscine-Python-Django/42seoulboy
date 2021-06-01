from os import environ

SECRET_KEY = "hekim2"

OMDB_API_KEY = (
    "2562735f"
    if environ.get("OMDB_API_KEY") is None
    else environ.get("OMDB_API_KEY")
)

GRID_SIZE = (14, 14)
SCREEN_SIZE = (10, 10)
SCREEN_OFFSET = (-5, -5)
PLAYER_INIT_POS = (5, 5)
PLAYER_INIT_MOVBALL = 20
MOVIEBALL_POP_PROB = 10

IMDB_DIVERSE = True

IMDB_LIST = [
    "tt0468492",
    "tt5034838",
    "tt0078748",
    "tt0087363",
    "tt0073195",
    "tt8235660",
    "tt0118615",
    "tt0105643",
    "tt1844770",
    "tt0329101",
    "tt0372873",
    "tt1934381",
    "tt1270797",
    "tt3967856",
    "tt10240612",
    "tt0317676",
    "tt1489946",
    "tt1714203",
    "tt5639976",
    "tt6644200",
    "tt0198781",
    "tt0091064",
    "tt4680182",
    "tt2231461",
    "tt0100814",
    "tt5688868",
    "tt4374286",
    "tt0069005",
    "tt0100260",
    "tt0089469",
    "tt0055894",
    "tt1396484",
    "tt0065163",
    "tt0090190",
    "tt0084745",
    "tt0457430",
    "tt0093177",
    "tt0083907",
    "tt5884052",
    "tt3794354",
    "tt7504864",
    "tt1415872",
    "tt7904362",
    "tt1788453",
]
IMDB_LIST_KOR = [
    "tt0272425",
    "tt0289181",
    "tt0327169",
    "tt0364569",
    "tt0406661",
    "tt0428870",
    "tt1606283",
    "tt2972482",
    "tt2990738",
    "tt4682562",
    "tt4844288",
    "tt5066556",
    "tt5068856",
    "tt5215952",
    "tt6890582",
    "tt6904062",
    "tt7046826",
    "tt7057496",
    "tt8290698",
    "tt8850222",
    "tt10530286",
    "tt11358398",
    "tt11777040",
]

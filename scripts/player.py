class Player:
    id = 0
    year = 0
    club = ""
    name = ""
    image = ""
    country = ""
    position = ""
    ovr = 0
    price = 0
    age = 0
    height = 0

    assists = 0
    goals = 0
    matches = 0
    cards = 0

    def __init__(self, year, club, name, image, country, id, position):
        self.year = year
        self.club = club
        self.name = name
        self.image = image
        self.country = country
        self.id = id
        self.position = position

    def add_infos(self, age, height, price, ovr):
        self.age = age
        self.height = height
        self.price = price
        self.ovr = ovr

    def add_stats(self, matches, goals, assists):
        self.goals = goals
        self.matches = matches
        self.assists = assists

    def __str__(self):
        string = f"\n{self.name} - id: {self.id} / {self.club}"
        string += f"\nposition: {self.position} country: {self.country} ovr: {self.ovr} age: {self.age} price: {self.price} height: {self.height} "
        string += "\n" + f"matches: {self.matches} gols: {self.goals} assists: {self.assists}"
        string += "\n" + self.image
        return string

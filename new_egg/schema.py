class NewEggItemData:
    def __init__(self, name: str, usd_price: float, gtin12: str, mpn: str, model: str, link: str):
        self.name: str = name
        self.price_usd: float = usd_price
        self.gtin12: str = gtin12
        self.mpn: str = mpn
        self.model: str = model
        self.link: str = link

    def __str__(self):
        return f"<NewEggItemData> name: {self.name}, price: {self.price_usd}, gtin12: {self.gtin12}, mpn: {self.mpn}, model: {self.model}"

    def __repr__(self):
        return self.__str__()

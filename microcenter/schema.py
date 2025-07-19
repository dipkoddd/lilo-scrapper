class MicroCenterItemData:
    def __init__(self, name: str, usd_price: float, link: str):
        self.name: str = name
        self.usd_price: str = usd_price
        self.link: str = link

    def __str__(self):
        return f"<MicroCenterItemData> name: {self.name}, price: {self.usd_price}"

    def __repr__(self):
        return self.__str__()

class WeatherReport:
    def _init_(self,temperature,humidity,pressure):
        self.temperature=temperature
        self.humidity=humidity
        self.pressure=pressure
    def toJSON(self):
        return {'Temperature: ':self.temperature,'<br /> Humidity: ':self.humidity,'<br /> Pressure: ':self.pressure}
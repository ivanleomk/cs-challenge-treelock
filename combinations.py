x = {'energy': 6, 'capital': 250, 'timeline': {'2037': {'Apple': {'price': 102, 'qty': 33}, 'BitCoin': {'price': 349, 'qty': 64}}, '2034': {'Apple': {'price': 113, 'qty': 54}, 'BitCoin': {'price': 298, 'qty': 42}}}}

def main(data_obj):
      stock_prices = data_obj['timeline']
      prices = [(stock_prices[key],key) for key in stock_prices.keys()]


def generate_combinations(data_obj):
      adj_graph = {}
      prices = data_obj['timeline']
      combinations = []
      
      years_sorted = list(prices.keys())
      years_sorted.sort()

      #Each individual stock in the year is matched to every other stock which it can 
      for year in years_sorted:
            print(year)

      return combinations

print(generate_combinations(x))
    



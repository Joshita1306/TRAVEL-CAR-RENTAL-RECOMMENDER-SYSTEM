from flask import Flask, render_template, request
import pandas as pd
import traceback

app = Flask(__name__)

def load_data():
    try:
        print("Loading attractions data...")
        attractions = pd.read_excel("data/attractions_info.xlsx")
        print(f"Attractions loaded. Columns: {attractions.columns.tolist()}")
        
        print("Loading hotels data...")
        hotels = pd.read_csv("data/hotel_info.csv", encoding='latin1')  # or 'ISO-8859-1', 'cp1252'
        print(f"Hotels loaded. Columns: {hotels.columns.tolist()}")
        
        print("Loading restaurants data...")
        encodings = ['utf-8', 'latin1', 'ISO-8859-1', 'cp1252']
        restaurants = None
        
        for encoding in encodings:
            try:
                restaurants = pd.read_csv("data/Restaurant_info_2.csv", encoding=encoding)
                restaurants.columns = restaurants.columns.str.strip()
                print(f"Restaurants loaded with {encoding}. Columns: {restaurants.columns.tolist()}")
                break
            except Exception as e:
                print(f"Failed with {encoding}: {str(e)}")
                continue
                
        if restaurants is None:
            raise ValueError("Could not load restaurant data with any encoding")
            
        return attractions, hotels, restaurants
        
    except Exception as e:
        print("CRITICAL ERROR LOADING DATA:")
        print(traceback.format_exc())
        return None, None, None

attractions_df, hotels_df, restaurants_df = load_data()

@app.route("/")
def index():
    return render_template("indexx.html")

@app.route("/results", methods=["POST"])
def results():
    try:
        # Debug: Print loaded data shapes
        print(f"\nData Shapes - Attractions: {attractions_df.shape if attractions_df is not None else 'None'}, "
              f"Hotels: {hotels_df.shape if hotels_df is not None else 'None'}, "
              f"Restaurants: {restaurants_df.shape if restaurants_df is not None else 'None'}")
        
        # Get user input with defaults
        destination = request.form.get("destination", "").strip().lower()
        cuisine_type = request.form.get("cuisine_type", "").strip().lower()
        
        # Initialize empty results
        restaurant_results = []
        hotel_results = []
        attraction_results = []
        
        # RESTAURANT FILTERING - WITH ROTATION
        if restaurants_df is not None and cuisine_type:
            try:
                print(f"\nFiltering restaurants for cuisine: {cuisine_type}")
                cuisine_pattern = '|'.join(cuisine_type).lower()
                all_matches = restaurants_df[restaurants_df['Type'].str.lower().str.contains(cuisine_type.lower(), na=False)]
        
        # Shuffle the results randomly
                shuffled_matches = all_matches.sample(frac=1)
        
        # Get first 6 (different each time due to shuffle)
                restaurant_results = shuffled_matches.head(6).to_dict('records')
        
                print(f"Found {len(restaurant_results)} restaurant matches (randomized)")
        
            except Exception as e:
                print(f"Restaurant filtering error: {str(e)}")
        
        # HOTEL FILTERING - MODIFIED FOR RANDOM SELECTION
        if hotels_df is not None:
            try:
                print("\nFiltering hotels...")
                filtered = hotels_df.copy()
                
                shuffled_matches = all_matches.sample(frac=1)
        
        # Price filtering
                if 'Price' in filtered.columns:
                    filtered['Price'] = pd.to_numeric(filtered['Price'], errors='coerce')
                    filtered = filtered.dropna(subset=['Price'])
                    print(f"After Price cleaning: {len(filtered)} matches")
        
        # Get random 6 hotels (or less if fewer available)
                    hotel_results = filtered.sample(min(6, len(filtered))).to_dict('records')
                    print(f"Final hotel results: {len(hotel_results)}")
        
            except Exception as e:
                print(f"Hotel filtering failed: {str(e)}")
                print(traceback.format_exc())
        
        # ATTRACTION FILTERING
        if attractions_df is not None:
            try:
                print("\nFiltering attractions...")
                print(f"Destination: {destination}")
                
                # Find location columns dynamically
                location_cols = [col for col in attractions_df.columns 
                               if col.lower() in ['location', 'city', 'address', 'region', 'area']]
                print(f"Using location columns: {location_cols}")
                
                # Create destination filter
                dest_filter = pd.Series(False, index=attractions_df.index)
                for col in location_cols:
                    if col in attractions_df.columns:
                        dest_filter |= attractions_df[col].astype(str).str.lower().str.contains(destination, na=False)
                
                filtered = attractions_df[dest_filter].copy() if not dest_filter.empty else pd.DataFrame()
                print(f"After location filter: {len(filtered)} matches")
                
                # Price filtering
                price_cols = [col for col in filtered.columns if 'price' in col.lower()]
                if price_cols:
                    price_col = price_cols[0]
                    filtered['price_numeric'] = pd.to_numeric(
                        filtered[price_col].astype(str).str.replace(r'[^\d.]', '', regex=True),
                        errors='coerce'
                    )
                    filtered = filtered.dropna(subset=['price_numeric'])
                    print(f"After price cleaning: {len(filtered)} matches")
                
                attraction_results = filtered.head(6).to_dict('records')
                print(f"Final attraction results: {len(attraction_results)}")
                
            except Exception as e:
                print(f"Attraction filtering failed: {str(e)}")
                print(traceback.format_exc())
        
        return render_template(
            "resultss.html",
            restaurants=restaurant_results,
            hotels=hotel_results,
            attractions=attraction_results,
            user_data={
                "destination": destination,
                "cuisine_type": cuisine_type
            }
        )
        
    except Exception as e:
        print(f"CRITICAL ERROR IN RESULTS: {str(e)}")
        print(traceback.format_exc())
        return render_template("error.html", message="A system error occurred. Please try again later.")

@app.route('/pay')
def payment_page():
    return render_template('pay.html')

if __name__ == "__main__":
    app.run(debug=True)
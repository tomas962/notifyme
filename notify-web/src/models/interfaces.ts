
interface CarQuery {
    city_id: number;
    id: number;
    power_from: number;
    power_to: number;
    price_from: number;
    price_to: number;
    search_term: string;
    user_id: number;
    year_from: number;
    year_to: number;
}

interface BodyStyle {
    autobilis_id: number;
    autoplius_id: number;
    id: number;
    name: string;
}

interface FuelType {
    autobilis_fuel_id: number;
    autoplius_fuel_id: number;
    fuel_name: string;
    id: number;
}

interface MakeModel {
    autobilis_make_id: number;
    autobilis_model_id: number;
    autoplius_make_id: number;
    autoplius_model_id: number;
    make_id: number;
    make: string;
    model_name: string;
    model_id: number;
}

interface CarQueryResponse {
    car_query: CarQuery;
    body_style: BodyStyle;
    fuel_type: FuelType;
    make_model: MakeModel;
}

interface NewCarQuery {
    make_id: number;
    model_id: number;
    city_id: number;
    power_from: number;
    power_to: number;
    search_term: string;
    year_to: number;
    year_from: number;
    
    /**body_styles.id in database */
    body_style_id: number;
    fuel_id: number;
    price_from: number;
    price_to: number;

}

interface Make {
    id: number;
    make: string;
}

export {
    CarQueryResponse,
    CarQuery,
    BodyStyle,
    FuelType,
    MakeModel,
    NewCarQuery,
    Make
}
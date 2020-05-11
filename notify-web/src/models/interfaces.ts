
interface CarQuery {
    city_id: number;
    city?: string;
    id: number;
    power_from: number;
    power_to: number;
    price_from: number;
    price_to: number;
    search_term: string;
    user_id: number;
    year_from: number;
    year_to: number;
    sites?: string;
    currently_scraping: number;
    last_scraped: number; 
    scrape_interval: number|null; 
    was_scraped: number;
    gearbox: null|string;
    driven_wheels: null|string;
    steering_column: null|string;
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
    [key: string]: any;
    make_id: number|null;
    model_id: number|null;
    city_id: number|null;
    power_from: number|null;
    power_to: number|null;
    search_term: string|null;
    year_to: number|null;
    year_from: number|null;
    gearbox: null|string;
    driven_wheels: null|string;
    steering_column: null|string;

    /**body_styles.id in database */
    body_style_id: number|null;
    fuel_id: number|null;
    price_from: number|null;
    price_to: number|null;
    sites: string[];
    query_id?: number|null;
}

interface Make {
    id: number;
    make: string;
}

interface MessageResponse {
    id: number;
    text: string;
    timestamp: string;
    title: string;
    user_id: number;
}


interface SelectOption {
    value: string|number|null;
    text: string;
}

export {
    CarQueryResponse,
    CarQuery,
    BodyStyle,
    FuelType,
    MakeModel,
    NewCarQuery,
    Make,
    MessageResponse,
    SelectOption
}
//Author: Oscar Reina, Burak Askan
export interface CompanyPrediction {
    company_code: string;
    company_name: string;
    prediction_value: number;
    tweet_rate: number;
    avg_sentiment: number;
    stock_val: number;
    created_at: string;
}

export function parseCompanyPredictions(jsonString: string): CompanyPrediction[] {
    try {
        const jsonArray: any[] = JSON.parse(jsonString);
        const companyPredictions: CompanyPrediction[] = jsonArray.map((item: any) => {
            return {
                company_code: item.company_code,
                company_name: item.company_name,
                prediction_value: item.prediction_value,
                tweet_rate: item.tweet_rate,
                avg_sentiment: item.avg_sentiment,
                stock_val: item.stock_val,
                created_at: item.created_at.toString(),
            };
        });
        return companyPredictions;
    } catch (error) {
        console.error("Error parsing JSON:", error);
        return [];
    }
}
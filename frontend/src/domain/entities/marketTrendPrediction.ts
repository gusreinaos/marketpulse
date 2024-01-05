//Author: Oscar Reina
export interface MarketTrendPredictionRequest {
    requestTimeStamp: Date;
    requestCompany: string;
}

export interface MarketTrendPredictionResponse {
    responseTimeStamp: Date;
    trendValue: number;
}
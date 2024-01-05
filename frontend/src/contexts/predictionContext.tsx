//Author: Oscar Reina
import React, { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { MarketTrendPredictionRequest, MarketTrendPredictionResponse } from "../domain/entities/marketTrendPrediction";
import ModelService from "../services/modelService";

interface ContextState {
  prediction: MarketTrendPredictionResponse | undefined;
  getCurrentModelPrediction: (marketTrendPredictionRequest: MarketTrendPredictionRequest) => Promise<MarketTrendPredictionResponse>;
}

interface PredictionContextProviderProps {
  children: ReactNode;
  marketTrendRequestData: MarketTrendPredictionRequest; 
}

export const PredictionContext = createContext({} as ContextState);

export const PredictionContextProvider: React.FC<PredictionContextProviderProps> = ({ children, marketTrendRequestData }) => {
  const [prediction, setPrediction] = useState<MarketTrendPredictionResponse | undefined>(undefined);

  const getCurrentModelPrediction = async () => {
    const response = await ModelService.getCurrentModelPrediction(marketTrendRequestData.requestCompany);
    setPrediction(response); 
    return response;
  };

  useEffect(() => {
    getCurrentModelPrediction();
  }, [marketTrendRequestData]);

  const contextValue: ContextState = {
    prediction,
    getCurrentModelPrediction,
  };

  return (
    <PredictionContext.Provider value={contextValue}>
      {children}
    </PredictionContext.Provider>
  );
};

export const usePredictionContext = () => {
  const context = useContext(PredictionContext);
  if (!context) {
    throw new Error("usePredictionContext must be used within a PredictionContextProvider");
  }
  return context;
};

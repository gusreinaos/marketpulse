//Author: Oscar Reina
import React, { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { MarketTrendPredictionRequest, MarketTrendPredictionResponse } from "../domain/entities/marketTrendPrediction";
import { StockRequest, StockResponse } from "../domain/entities/stock";
import CompanyService from "../services/companyService";

interface ContextState {
  stockValues: StockResponse | undefined;
  getCompanyStockValues: (stockRequest: StockRequest) => Promise<StockResponse>;
}

interface CompanyContextProviderProps {
  children: ReactNode;
  stockRequestData: StockRequest; 
}

export const CompanyContext = createContext({} as ContextState);

export const CompanyContextProvider: React.FC<CompanyContextProviderProps> = ({ children, stockRequestData }) => {
  const [stockValues, setStockValues] = useState<StockResponse | undefined>(undefined);

  const getCompanyStockValues = async () => {
    const response = await CompanyService.getCompanyHistory(stockRequestData.requestCompany);
    setStockValues(response); 
    return response;
  };

  useEffect(() => {
    getCompanyStockValues();
  }, []);

  const contextValue: ContextState = {
    stockValues,
    getCompanyStockValues,
  };

  return (
    <CompanyContext.Provider value={contextValue}>
      {children}
    </CompanyContext.Provider>
  );
};

export const usePredictionContext = () => {
  const context = useContext(CompanyContext);
  if (!context) {
    throw new Error("usePredictionContext must be used within a PredictionContextProvider");
  }
  return context;
};


//Author: Aditya Khadkikar, Wojciech Pechmann
import axios from 'axios';
import { CompanyPrediction } from '../domain/entities/companyPrediction';
import SortUtils from '../components/customer/sorting_utl'


const API_BASE_URL = 'http://34.122.134.118:8000'; 

const ModelService = {
    getCurrentModelPrediction: async (requestCompany: string) => {
        try {
            const response = await axios.get(`${API_BASE_URL}/api/predictions/${requestCompany}`);
            return response.data;
        }
        catch(error: any) {
            console.log(error)
        }
    },
    getRegularModelPrediction: async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/api/models`);
            return response.data;
        }
        catch(error: any) {
            throw error.response.data;
        }
    },
    getSentimentModels: async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/api/admins/models/sentiment`);
            return response.data; 
        } catch (error: any) {
            console.log(error); 
        }
    },
    getSentimentModel: async (modelVersion: string) => {
        try {
            const response = await axios.get(`${API_BASE_URL}/api/admins/models/sentiment/${modelVersion}`);
            return response.data; 
        } catch (error: any) {
            console.log(error); 
        }
    },
    getSentimentProductionModel: async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/api/admins/models/sentiment-production`);
            return response.data; 
        } catch (error: any) {
            console.log(error); 
        }
    },
    trainSentimentModel: async (modelVersion: string, file: FormData) => {
        try {
            console.log(modelVersion);    
            const rest = await axios.post(`${API_BASE_URL}/api/admins/models/sentiment/${modelVersion}/train`, file, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
            return rest.data.response
        } catch (error: any) {
            console.log(error);
            return 'false'
        }
    },
    getMarketTrendModels: async () => {
        try {
            const response = await axios.get(`${API_BASE_URL}/api/admins/models/trend`);
            return response.data; 
        } catch (error: any) {
            console.log(error); 
        }
    },
    getMarketTrendModel: async (modelVersion: string) => {
        try {
            const response = await axios.get(`${API_BASE_URL}/api/admins/models/trend/${modelVersion}`);
            return response.data; 
        } catch (error: any) {
            console.log(error); 
        }
    },
    getMarketTrendProductionModel: async () => {
        //MAKE SURE TO FIX ENDPOINT AS IT IS SIMILAR TO SENTIMENT MODEL ENDPOINT -> Fixed?
        try {
            const response = await axios.get(`${API_BASE_URL}/api/admins/models/trend-prodcution`);
            return response.data; 
        } catch (error: any) {
            console.log(error); 
        }
    },
    trainMarketTrendModel: async (modelVersion: string, file: FormData) => {
        try {
            console.log(modelVersion);    
            const rest = await axios.post(`${API_BASE_URL}/api/admins/models/trend/${modelVersion}/train`, file, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })

            return rest.data.response
        } catch (error: any) {
            console.log(error);
            return 'false'
        }
    },
    setPredictionTrendModel: async (modelVersion: string) => {
        //MAKE SURE TO FIX ENDPOINT AS IT IS SIMILAR TO SENTIMENT MODEL ENDPOINT
        try {
            console.log(modelVersion);    
            const response = axios.post(`${API_BASE_URL}/api/admins/models/trend/set/${modelVersion}`)
            return response

        } catch (error: any) {
            console.log(error);
        }
    },
    setPredictionSentimentModel: async (modelVersion: string) => {
        //MAKE SURE TO FIX ENDPOINT AS IT IS SIMILAR TO SENTIMENT MODEL ENDPOINT
        try {
            console.log(modelVersion);    
            const response = axios.post(`${API_BASE_URL}/api/admins/models/sentiment/set/${modelVersion}`)
            return response

        } catch (error: any) {
            console.log(error);
        }
    },
    getLatestPredictions: async (customerId: string) => {
        try {
            //const response = await axios.get(`${API_BASE_URL}/api/customers/${customerId}/favorites`)
            
           const response = await axios.get(`${API_BASE_URL}/api/companies`)
            const list = eval(response.data) as CompanyPrediction[];
            
            const sorted = SortUtils.sentiment_sort(list)

            return sorted;
        } catch(error: any){
            throw error.response.data;
        }
    },
    getRefreshedPredictions: async (requestCompany: string, timeStamp: number) => {
        try {
            const response = await axios.get(`${API_BASE_URL}/api/predictions/${requestCompany}`,{
                params: {
                    timestamp: timeStamp
                }
            })
            
            return response.data
        } catch(error: any) {
            throw error.response.data;
        }
    }
}

export default ModelService;
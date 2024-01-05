//Author: Michael Larsson
import axios from 'axios'

export interface Company {
    companyCode: string;
}

const API_BASE_URL = 'http://34.122.134.118:8000'

const CompanyService = {
    getCompanyHistory: async (companyCode: string) => {
        try{
            const response = await axios.get(`${API_BASE_URL}/api/companies/history/${companyCode}`)
            return response.data
        } catch (error: any){
            throw error.response.data
        }
    },

    getCurrentStockTrend: async (companyCode: string) => {
        try{
            const response = await axios.get(`${API_BASE_URL}/api/companies/stockTrend/${companyCode}`)
            return response.data
        } catch (error: any){
            throw error.response.data
        }
    },


    getCurrentInflationTrend: async () => {
        try{
            const response = await axios.get(`${API_BASE_URL}/api/companies/inflationTrend/`)
            return response.data
        } catch (error: any){
            throw error.response.data
        }
    },

    getCompanyTestimonials: async (companyCode : string) => {
        try{ 
            const response = await axios.get(`${API_BASE_URL}/api/companies/testimonials/${companyCode}`)
            return response.data
        } catch (error: any){
            throw error.response.data
        }
    },

    getCompanyInfo: async (companyCode: string) => {
        try{
            const response = await axios.get(`${API_BASE_URL}/api/companies/info/${companyCode}`)
            return response.data
        } catch (error: any){
            throw error.response.data
        }
    }
}

export default CompanyService
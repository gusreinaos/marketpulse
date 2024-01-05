//Author: Burak Askan, Wojciech Pechmann
import {CompanyPrediction} from  '../../domain/entities/companyPrediction'

class SortUtils {

    static stock_sort(jsonData: CompanyPrediction[],isReversed: boolean=false): CompanyPrediction[] {
        const tsArray: CompanyPrediction[] = jsonData;
      
        const sortedCompanies = isReversed?   tsArray.slice().sort((a, b) => a.stock_val - b.stock_val):tsArray.slice().sort((a, b) => b.stock_val - a.stock_val);
      
        return sortedCompanies;
    }
      
     
    static predicton_sort(jsonData: CompanyPrediction[],isReversed: boolean=false): CompanyPrediction[] {
        const tsArray: CompanyPrediction[] = jsonData;
      
        const sortedCompanies = !isReversed?   tsArray.slice().sort((a, b) => a.prediction_value - b.prediction_value):tsArray.slice().sort((a, b) => b.prediction_value - a.prediction_value);
      
        return sortedCompanies;
    }

  
    static sentiment_sort(jsonData: CompanyPrediction[], isReversed:boolean=false): CompanyPrediction[] {
        const tsArray: CompanyPrediction[] = jsonData;
      
        const sortedCompanies = !isReversed?   tsArray.slice().sort((a, b) => a.avg_sentiment - b.avg_sentiment) : tsArray.slice().sort((a, b) => b.avg_sentiment - a.avg_sentiment);
      
        return sortedCompanies;
    }
      
      
  
    static tweet_rate_sort(jsonData: CompanyPrediction[], isReversed:boolean=false): CompanyPrediction[] {
        const tsArray: CompanyPrediction[] = jsonData;
      
        const sortedCompanies = !isReversed?  tsArray.slice().sort((a, b) => a.tweet_rate - b.tweet_rate) : tsArray.slice().sort((a, b) => b.tweet_rate - a.tweet_rate);
      
        return sortedCompanies;
    }

    
    static name_sort(jsonData: CompanyPrediction[], isReversed:boolean=false): CompanyPrediction[] {
        const tsArray: CompanyPrediction[] = jsonData;
    
        const sortedCompanies = !isReversed?  tsArray.slice().sort((a, b) => a.company_name.localeCompare(b.company_name)) : tsArray.slice().sort((a, b) => b.company_name.localeCompare(a.company_name));
    
        return sortedCompanies;
    }
    
      
  }
  
  export default SortUtils;
  
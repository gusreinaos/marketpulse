//Author: Wojciech Pechmann

import styles from './fav-button-component.module.scss';
import { Button } from 'react-bootstrap';
import customerService from '../../../services/customerService';
import React, { useContext, useEffect, useState, useRef  } from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import CompanyService from '../../../services/companyService';
import { AuthContext } from '../../../contexts/authContext';
import { CompanyPrediction } from '../../../domain/entities/companyPrediction';


interface FavBtnProbs {
  data:{
    company_id: string
  }
}


//TODO: check if if(response) behaves as expected or needs to be changed

const FavButton: React.FC<FavBtnProbs> = ({data}) => {
  const [isFavorite, setFavorite] = useState(false)
  
  const authContext = useContext(AuthContext);
  const navigate = useNavigate();


  const contextValue = useContext(AuthContext);

  const id = contextValue?.user?.id;

  const [hasRun, setRun] = useState(false);


  const getCompanyList = async () => {
    try {
      const list_companies = await customerService.getCustomerFavorites(id?id:'');
     
      console.log('COMP:',list_companies)

      setFavorite(false)
      list_companies.forEach((entry: CompanyPrediction) => {
        if(entry.company_code===data.company_id){
          setFavorite(true)
        } 
      })

      setRun(true)

    } catch (error) {
      console.error('Error fetching inflation trend:', error);
    }
  };



  if(!hasRun){
    getCompanyList();
  }

  const favoriteCompany = async () => {
    if(isFavorite){
      
      try{
        const response = await customerService.removeCustomerFavoriteCompany(id?id:'',data.company_id);
        
        if(response){
          setFavorite(false)
        }

      }catch(error){
        console.error('Error favoriting: ',error)
      }
      
      

    }else {
      try{
        const response = await customerService.addCustomerFavoriteCompany(id?id:'',data.company_id);
      
        if(response){
          setFavorite(true)
        }
      
      }catch(error){
        console.error('Error favoriting: ',error)
      }
    }
    
  }

  
  return (
    
    <div >

      {
        isFavorite?
        <div className={styles.normal_mouse} onClick={favoriteCompany}>⭐</div>
        : <div className={styles.normal_mouse} onClick={favoriteCompany}>✰</div>
      }
    </div>
  ) 
}
export default FavButton;
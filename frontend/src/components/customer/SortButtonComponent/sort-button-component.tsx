//Author: Wojciech Pechmann

import styles from './sort-button-component.module.scss';
import { Button } from 'react-bootstrap';
import customerService from '../../../services/customerService';
import React, { useContext, useEffect, useState, useRef  } from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import CompanyService from '../../../services/companyService';
import { AuthContext } from '../../../contexts/authContext';
import { CompanyPrediction } from '../../../domain/entities/companyPrediction';
import { SortState } from '../../../domain/entities/sortState';



interface SortButtonProbs {
  data:{
    sort_func: any
    list: CompanyPrediction[]
    update_func: any
    name: string
    list_state?: SortState
    callback?: any
  }
}


//TODO: check if if(response) behaves as expected or needs to be changed

const SortButton: React.FC<SortButtonProbs> = ({data}) => {

  const sort = () =>{
    

    if(data.callback != null && data.list_state != null){
      let reverse_sort = false

      if(data.list_state.column === data.name){
        reverse_sort = data.list_state.nextInReverse;
      }
      
      console.log(data.list_state)

      data.update_func(data.sort_func(data.list, reverse_sort))

      data.callback()
    } else {
      data.update_func(data.sort_func(data.list))
    }
  }


  
  return (
    
    <div className={styles.normal_mouse} onClick={sort} >

    {data.name}

    </div>
  ) 
}
export default SortButton;
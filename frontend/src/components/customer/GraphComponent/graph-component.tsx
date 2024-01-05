//Author: Michael Larsson, Oscar Reina

import React, { useEffect, useRef } from 'react';
import { createChart } from 'lightweight-charts';
import styles from './graph-component.module.scss';

interface ChartProps {
  data: { time: string; value: number }[];
}

const Chart: React.FC<ChartProps> = ({ data }) => {
  const chartContainerRef = useRef<HTMLDivElement | null>(null);
  const chartRef = useRef<any | null>(null);

  useEffect(() => {
    const createChartInstance = async () => {
      try {
        if (chartContainerRef.current) {
          if (chartRef.current) {
            chartRef.current.remove();
          }

          const parentWidth = chartContainerRef.current.offsetWidth;

          chartRef.current = createChart(chartContainerRef.current!, {
            width: parentWidth,
            height: 350,
            rightPriceScale: {
              scaleMargins: {
                top: 0.2,
                bottom: 0.2,
              },
              borderVisible: false,
            },
            timeScale: {
              borderVisible: false,
            },
            grid: {
              horzLines: {
                color: '#eee',
              },
              vertLines: {
                color: '#ffffff',
              },
            },
            crosshair: {
              vertLine: {
                labelVisible: false,
              },
            },
          });

          const lineSeries = chartRef.current.addAreaSeries({
            priceLineVisible: true,
            priceLineWidth: 2,
            priceLineColor: 'rgba(17, 73, 123, 1)',
            baseLineVisible: true,
            baseLineWidth: 2,
            baseLineColor: 'rgba(17, 73, 123, 1)',
            lineColor: `rgb(2,179,255)`, 
            topColor: `rgba(2,179,255, 0.5)`, 
            bottomColor:`rgba(2,179,255, 0)`,
          });
          
          lineSeries.setData(data);

          lineSeries.applyOptions({
            priceLineVisible: true,
            priceLineWidth: 2,
            priceLineColor: 'black',
            baseLineVisible: true,
            baseLineWidth: 2,
            baseLineColor: 'black',
            lastPriceAnimation: {
              animationEnabled: true,
              duration: 300,
              mode: 2, // 'to-the-end' mode
            },
          });
        }
      } catch (error) {
        console.error('An error occurred while fetching data:', error);
      }
    };

    createChartInstance();
  }, [data]); // Run the effect whenever 'data' changes

  useEffect(() => {
    const handleResize = () => {
      if (chartRef.current) {
        const parentWidth = chartRef.current.offsetWidth;
        chartRef.current.resize(parentWidth, 400);
      }
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  return (
    <div>
      <h5 className={styles.chartTitle}>Closing Price History</h5>
      <div ref={chartContainerRef}></div>
    </div>
  );
};

export default Chart;

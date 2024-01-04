import { useState } from 'react';

export const useHamburger = () => {
  const [hamburger, setHamburger] = useState(false);
  const [slideOut, setSlideOut] = useState(false);
  const [slideIn, setSlideIn] = useState(false);

  const toggleHamburger = () => {
    if (hamburger) {
      setSlideIn(false);
      setSlideOut(true);
      setTimeout(() => {
        setHamburger(false);
      }, 200);
    } else {
      setSlideIn(true);
      setSlideOut(false);
      setHamburger(true);
    }
  };

  return { hamburger, toggleHamburger, slideIn, slideOut };
};

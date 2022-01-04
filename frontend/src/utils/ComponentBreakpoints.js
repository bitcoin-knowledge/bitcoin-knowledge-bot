import { css } from "styled-components"
const sizes = {
  widescreen: 1366,
  desktop: 1200,
  laptop: 1024,
  tablet: 768,
  phone: 480,
  tiny: 100,
}
export default Object.keys(sizes).reduce((acc, label) => {
  acc[label] = (...args) => css`
    @media (max-width: ${sizes[label]}px) {
      ${css(...args)};
    }
  `
  return acc
}, {})
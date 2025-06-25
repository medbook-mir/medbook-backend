'use client'

import styled from 'styled-components'

const Loading = () => {
  return (
    <CustomLoading>
      <span className="loader"></span>
    </CustomLoading>
  )
}

export default Loading

const CustomLoading = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  height: 80vh;

  .loader {
    width: 48px;
    height: 48px;
    border: 5px solid #046d5f;
    border-bottom-color: transparent;
    border-radius: 50%;
    display: inline-block;
    box-sizing: border-box;
    animation: rotation 1s linear infinite;
  }

  @keyframes rotation {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
`

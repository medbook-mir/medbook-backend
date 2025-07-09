'use client'

import React from 'react'
import { ReactNode, useEffect } from 'react'
import { motion, useAnimation, useReducedMotion, Variants } from 'framer-motion'
import { useInView } from 'react-intersection-observer'

interface AnimatedInViewProps {
  children: ReactNode
  direction?: 'up' | 'down' | 'left' | 'right'
  variant?: 'fade' | 'slide' | 'scale'
  delay?: number
  duration?: number
  offset?: number
  triggerOnce?: boolean
  staggerChildren?: boolean
  staggerDelay?: number
  as?: keyof React.JSX.IntrinsicElements
}

export default function AnimatedInView({
  children,
  direction = 'up',
  variant = 'slide',
  delay = 0,
  duration = 0.6,
  offset = 50,
  triggerOnce = true,
  staggerChildren = false,
  staggerDelay = 0.15,
  as = 'div'
}: AnimatedInViewProps) {
  const controls = useAnimation()
  const [ref, inView] = useInView({
    triggerOnce,
    threshold: 0.2
  })
  const shouldReduceMotion = useReducedMotion()

  useEffect(() => {
    if (inView) {
      controls.start('visible')
    }
  }, [controls, inView])

  if (shouldReduceMotion) {
    return React.createElement(as, { ref }, children)
  }

  // Determine initial transform based on direction
  const directionOffset = {
    x: direction === 'left' ? offset : direction === 'right' ? -offset : 0,
    y: direction === 'up' ? offset : direction === 'down' ? -offset : 0
  }

  const variants: Variants = {
    hidden: {
      opacity: variant === 'fade' || variant === 'slide' || variant === 'scale' ? 0 : 1,
      scale: variant === 'scale' ? 0.9 : 1,
      x: variant === 'slide' ? directionOffset.x : 0,
      y: variant === 'slide' ? directionOffset.y : 0
    },
    visible: {
      opacity: 1,
      scale: 1,
      x: 0,
      y: 0,
      transition: {
        duration,
        ease: 'easeOut',
        delay,
        staggerChildren: staggerChildren ? staggerDelay : undefined
      }
    }
  }

  const MotionTag = motion[as as keyof typeof motion] as React.ElementType

  return (
    <MotionTag ref={ref} initial="hidden" animate={controls} variants={variants}>
      {children}
    </MotionTag>
  )
}

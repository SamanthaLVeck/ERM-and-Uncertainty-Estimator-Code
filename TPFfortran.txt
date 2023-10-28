!---------------------------------------------------------------------!
!                        Subroutine SDVINI
!      
!     Author: Samantha Veck
!      
!     Date: 24 November 2021
!
!---------------------------------------------------------------------!
!
!     Notes:
!
!     Subroutine SDVINI to determine the initial values for solution
!     dependent state variables (statev(*)) where 1=x, 2=y, 3=z.
!     Stores the coordinates of the nodes so they can 
!     be used with UEXPAN.
!
!---------------------------------------------------------------------!
      subroutine sdvini(statev,coords,nstatv,ncrds,noel,npt,layer,kspt)

      include 'aba_param.inc'

      dimension statev(nstatv),coords(ncrds)

      statev(1) = coords(1)
      statev(2) = coords(2)
      statev(3) = coords(3)

      return
      end

!---------------------------------------------------------------------!
!                        Subroutine UEXPAN
!      
!     Author: Samantha Veck
!      
!     Date: 15 June 2022
!
!---------------------------------------------------------------------!
!
!     Notes:
!     
!     This subroutine generates an eigenstrain field in one direction
!     using thermal expansion coefficients.
!      
!     The eigenstrain field is given by a triangular pulse function
!     which is iteratively applied as a job to the same model by 
!     seperate .for files. 
!
!        W - measurement axis width in mm 
!        N - number of basis functions
!        Z - order number of input file 
!
!     ck = arbritary coefficient set at 0.001
!
!    This file is updated for each basis function using the python 
!    code GenerateFortran.py. 
!
!---------------------------------------------------------------------!
      subroutine uexpan(expan,dexpandt,temp,time,dtime,predef,dpred,
     $     statev,cmname,nstatv,noel)

      include 'aba_param.inc'
      
      parameter (up_limit = )
      parameter (low_limit = )
      parameter (W = )
      parameter (N = )
      parameter (Z = )
      parameter (ck = 0.001) 
      
      character*80 cmname

      dimension expan(*),dexpandt(*),temp(2),time(2),predef(*),
     $     dpred(*),statev(nstatv)

      do I = 1,3
          dexpandt(I) = 0
      end do
      
!---------------------------------------------------------------------!
!
!     Notes:
!     
!     Definition of expansion coefficients and triangular pulse
!     function code. 
!
!     UPDATE FOR EACH ITERATION: 
!      - expan(*) 1,2,3 (11, 22, 33) based on component required
!      - statev(*) 1,2,3 (11, 22, 33) based on coord being used    
!
!     a = rising edge position
!     b = function peak position
!     c = falling edge position
!
!---------------------------------------------------------------------!
      
       expan(2) = 0.0D0
       expan(3) = 0.0D0
      
      a = 
      b = 
      c = 
       
      if ((statev(2).GE.a).and.(statev(2).LE.b)) then
          expan(1) = ((( statev(2) - a )/( b - a ))* ck )
      else if ((statev(2).GE.b).and.(statev(2).LE.c)) then 
          expan(1) = ((( c - statev(2) )/( c - b ))* ck )
      end if 
      
!---------------------------------------------------------------------!
!
!     Notes:
!     
!     Updating the solution dependant state variables 
!
!---------------------------------------------------------------------!
    
      statev(1) = statev(1)
      statev(2) = statev(2)
      statev(3) = statev(3)
      statev(4) = expan(1)
      statev(5) = expan(2)
      statev(6) = expan(3)
      
      do I = 1,3
          if (time(2).LE.1.0D0) then
              expan(I) = expan(I) * dtime 
          else
              expan(I) = 0.0D0
          end if
      end do
      
      return 
      end 
      
!---------------------------------------------------------------------------------------------------------------------------!
      

      
          
      
      
      
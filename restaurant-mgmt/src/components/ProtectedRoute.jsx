import { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';


import React from 'react';


export default function ProtectedRoute({
                                           children,
                                           
                                       }) {
    const [authState, setAuthState] = useState({
        isAuthenticated: false,
        loading: true,
        checked: false,
        userRole: null
    });

    
    const location = useLocation();

    useEffect(() => {
        let isMounted = true;

        const checkAuth = async () => {
            try {
                const verification =  true;

                if (isMounted) {
                    setAuthState({
                        isAuthenticated: true,
                        loading: false,
                        checked: true,
                       
                    });
                    
                }
            }
            catch (error) {
                if (isMounted) {
                    setAuthState({
                        isAuthenticated: false,
                        loading: false,
                        checked: true,
                        userRole: null
                    });
                    console.error(error);
                }
            }
        };

        checkAuth();

        return () => {
            isMounted = false;
        };
    }, [location.pathname]);

    if (authState.loading) {
        return (
            <div className="flex justify-center items-center h-screen">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
            </div>
        );
    }

    if (!authState.isAuthenticated && authState.checked) {
        return <AuthError />;
    }

    

  

   
    return (
       
            children
      
    );
}

function AuthError() {
    return (
      <div className="min-h-screen flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-red-50 border-l-6 border-red-500 p-6 rounded-lg shadow-md">
          <div className="flex items-center">
            <div className="flex-shrink-0">
              <svg className="h-5 w-5 text-red-500" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
              </svg>
            </div>
            <div className="ml-4">
              <h3 className="text-lg font-medium text-red-800">Access Denied</h3>
              <div className="mt-2 text-sm text-red-700">
                <p>You must be logged in with the correct permissions to view this page.</p>
              </div>
              <div className="mt-4">
                <button
                  onClick={() => window.location.href = '/login/Public'}
                  className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
                >
                  Go to Login
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
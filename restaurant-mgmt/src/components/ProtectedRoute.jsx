import { useEffect, useState } from 'react';
import { useLocation, Navigate } from 'react-router-dom';
import React from 'react';

function ProtectedRoute({ children })  {
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
              
                const response = await fetch('http://localhost:5002/api/verify_jwt', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                
                    },
                    credentials: 'include' 
                });

                if (response.ok) {
                    const data = await response.json();
                    if (isMounted && data.success) {
                        setAuthState({
                            isAuthenticated: true,
                            loading: false,
                            checked: true,
                       
                        });
                    } else if (isMounted) {
                        setAuthState({
                            isAuthenticated: false,
                            loading: false,
                            checked: true,
                            userRole: null
                        });
                    }
                }
                else {
                    if (isMounted) {
                        setAuthState({
                            isAuthenticated: false,
                            loading: false,
                            checked: true,
                            userRole: null
                        });
                    }
                }
            } catch (error) {
                if (isMounted) {
                    setAuthState({
                        isAuthenticated: false,
                        loading: false,
                        checked: true,
                        userRole: null
                    });
                    console.error("Error verifying token:", error);
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
        return <Navigate to="/login" />; 
    }



    return (

        children

    );
};

export default ProtectedRoute;

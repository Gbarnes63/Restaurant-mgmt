import { useState, useEffect } from 'react';
import { FiUser, FiLock, FiLogIn } from 'react-icons/fi';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function LoginSection({ loginType }) {
  const [loginStatus, setLoginStatus] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [authState, setAuthState] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const verifyAuthState = async () => {
      try {
    
        const response = await axios.post('http://localhost:5002/api/login', {
            username: 'dummyuser', 
            password: 'dummypassword', 
        },
        {
          withCredentials: true, // Ensure cookies are sent
        });
        setAuthState(response.data.success);
      } catch (error) {
        console.error('Error fetching data:', error);
        setAuthState(false);
      }
    };

    verifyAuthState();
  }, []);

  console.log(authState);

  if (authState) {
    navigate('/home');

  }

  // Ensure axios sends cookies with all requests
  axios.defaults.withCredentials = true;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setLoginStatus(null);

    const formData = new FormData(e.target);
    const loginData = {
      username: formData.get('username'),
      password: formData.get('password'), // In a real app, this should be hashed
    };

    try {
      // Send username and password to /api/login
      const response = await axios.post('http://localhost:5002/api/login', loginData);

      if (response.data.success) {
        setLoginStatus('success');
        navigate('/'); 
      } else {
        setLoginStatus('failed');
      }
    } catch (error) {
      if (error.response && error.response.status === 401) {
        setLoginStatus('failed');
      } else {
        setLoginStatus('error');
      }
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div
      className={`min-h-screen transition-colors duration-1000 ease-in-out flex items-center justify-center p-4 
    `}
    >
      <div className="w-1/3 rounded-2xl shadow-xl  bg-[#5B775B] backdrop-blur-sm">
        <div className="px-6 py-8">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold text-white mb-2">{loginType} Login</h2>
            <p className="text-gray-300">Login to Restaurant Management System</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            {loginStatus === 'failed' && (
              <div className="bg-red-500/40 border border-red-500/30 text-red-200 p-3 rounded-lg">
                Login failed. Please check your credentials.
              </div>
            )}
            {loginStatus === 'error' && (
              <div className="bg-red-500/40 border border-red-500/30 text-red-200 p-3 rounded-lg">
                An error occurred. Please try again later.
              </div>
            )}

            <div className="flex items-center justify-evenly">
              <label htmlFor="username" className="block text-sm font-medium text-gray-300">
                Username:
              </label>
              <div className="relative">
                <input
                  type="text"
                  id="username"
                  name="username"
                  required
                  className="w-full pl-10 pr-4 py-3 bg-white border border-gray-600 rounded-xl  placeholder-gray-400 text-gray-600"
                  placeholder="Enter your username"
                />
                <FiUser className="absolute left-3 top-3.5 text-gray-400" />
              </div>
            </div>

            <div className="flex items-center justify-evenly">
              <label htmlFor="login-password" className="block text-sm font-medium text-gray-300 ">
                Password
              </label>
              <div className="relative">
                <input
                  type="password"
                  id="login-password"
                  name="password"
                  required
                  className="w-full pl-10 pr-4 py-3 bg-white border border-gray-600 rounded-xl  placeholder-gray-400 text-gray-600 "
                  placeholder="Enter your password"
                />
                <FiLock className="absolute left-3 top-3.5 text-gray-400" />
              </div>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className={`w-full flex items-center justify-center px-6 py-3 rounded-lg transition-colors duration-300 ${
                isSubmitting
                  ? 'bg-blue-700 cursor-not-allowed'
                  : 'bg-[#A9DDA9] hover:bg-blue-700'
              } text-white`}
            >
              {isSubmitting ? (
                <>
                  <svg
                    className="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    ></circle>
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    ></path>
                  </svg>
                  Signing in...
                </>
              ) : (
                <>
                  <FiLogIn className="mr-2" />
                  <p className="font-bold text-teal-900">Login</p>
                </>
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}


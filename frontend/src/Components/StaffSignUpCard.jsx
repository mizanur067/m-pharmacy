import React,{ useState } from 'react'
import { useNavigate, Link } from 'react-router-dom';
import './CCS/UserSignUp.css';
const StaffSignUpCard = () => {
  const navigate = useNavigate();
  
    const [form, setForm] = useState({
      name: '',
      email: '',
      phone: '',
      address: '',
      password: '',
      confirmPassword: ''
    });
  
    const [showPassword, setShowPassword] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');
  
    const handleChange = (e) => {
      setForm({
        ...form,
        [e.target.name]: e.target.value
      });
      setError('');
    };
  
    const handleSubmit = async (e) => {
      e.preventDefault();
  
      if (form.password !== form.confirmPassword) {
        setError('Passwords do not match!');
        return;
      }
  
      if (form.password.length < 8) {
        setError('Password must contain at least 8 characters.');
        return;
      }
  
      setLoading(true);
      setError('');
      setSuccess('');
  
      try {
        const response = await fetch(
          'http://127.0.0.1:8000/Mizanur/staff-signup/',
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              name: form.name,
              email: form.email,
              phone: form.phone,
              address: form.address,
              password: form.password
            })
          }
        );
  
        const data = await response.json();
  
        if (!response.ok) {
          throw new Error(
            data.message || data.error || 'Registration failed!'
          );
        }
  
        setSuccess('Account created successfully!');
  
        setForm({
          name: '',
          email: '',
          phone: '',
          address: '',
          password: '',
          confirmPassword: ''
        });
  
        setTimeout(() => navigate('/user-login'), 1500);
  
      } catch (err) {
        setError(err.message || 'Something went wrong!');
      } finally {
        setLoading(false);
      }
    };
  
    return (
      <div className="signup_page_mpharmacy">
  
        <div className="signup_card_mpharmacy">
  
          <div className="signup_heading_mpharmacy">
            <div className="signup_logo_mpharmacy">
              <i className="fa-solid fa-heart-pulse"></i>
            </div>
  
            <h2>Create Account</h2>
            <p>Join M-Pharmacy for better healthcare.</p>
          </div>
  
          {error && (
            <div className="signup_error_mpharmacy">
              {error}
            </div>
          )}
  
          {success && (
            <div className="signup_success_mpharmacy">
              {success}
            </div>
          )}
  
          <form onSubmit={handleSubmit}>
  
            <div className="signup_input_group_mpharmacy">
              <label>Full Name</label>
              <div className="signup_input_mpharmacy">
                <i className="fa-regular fa-user"></i>
                <input
                  type="text"
                  name="name"
                  placeholder="Enter your full name"
                  value={form.name}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>
  
            <div className="signup_input_group_mpharmacy">
              <label>Email Address</label>
              <div className="signup_input_mpharmacy">
                <i className="fa-regular fa-envelope"></i>
                <input
                  type="email"
                  name="email"
                  placeholder="Enter your email"
                  value={form.email}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>
  
            <div className="signup_input_group_mpharmacy">
              <label>Phone Number</label>
              <div className="signup_input_mpharmacy">
                <i className="fa-solid fa-phone"></i>
                <input
                  type="tel"
                  name="phone"
                  placeholder="Enter your phone number"
                  value={form.phone}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>


            
            <div className="signup_input_group_mpharmacy">
            <label>Address</label>
            <div className="signup_input_mpharmacy">
              <i className="fa-solid fa-phone"></i>
              <input
                type="text"
                name="address"
                placeholder="Enter your address"
                value={form.address}
                onChange={handleChange}
                required
              />
            </div>
          </div>

            <div className="signup_input_group_mpharmacy">
              <label>Password</label>
              <div className="signup_input_mpharmacy">
                <i className="fa-solid fa-lock"></i>
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="password"
                  placeholder="Create a password"
                  value={form.password}
                  onChange={handleChange}
                  minLength={8}
                  required
                />
  
                <i
                  className={`fa-regular ${
                    showPassword ? 'fa-eye-slash' : 'fa-eye'
                  } signup_eye_mpharmacy`}
                  onClick={() => setShowPassword(!showPassword)}
                ></i>
              </div>
            </div>
  
            <div className="signup_input_group_mpharmacy">
              <label>Confirm Password</label>
              <div className="signup_input_mpharmacy">
                <i className="fa-solid fa-lock"></i>
                <input
                  type={showPassword ? 'text' : 'password'}
                  name="confirmPassword"
                  placeholder="Confirm your password"
                  value={form.confirmPassword}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>
  
            <button
              type="submit"
              className="signup_button_mpharmacy"
              disabled={loading}
            >
              {loading ? 'Creating Account...' : 'Create Account'}
              {!loading && <i className="fa-solid fa-arrow-right"></i>}
            </button>
  
          </form>
  
          <div className="signup_footer_mpharmacy">
            Already have an account?
            <Link to="/staff-login"> Login</Link>
          </div>
  
        </div>
  
      </div>
    );
}

export default StaffSignUpCard
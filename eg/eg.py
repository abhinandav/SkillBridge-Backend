# import React from 'react';
# import { useNavigate } from 'react-router-dom';
# import axios from 'axios';

# const TeacherSignup = () => {
#   const baseURL = 'http://127.0.0.1:8000';
#   const navigate = useNavigate();

#   const handleFormSubmit = async (event) => {
#     event.preventDefault();

#     const formData = new FormData();
#     formData.append('username', event.target.username.value);
#     formData.append('email', event.target.email.value);
#     formData.append('password', event.target.password.value);
#     formData.append('cpassword', event.target.cpassword.value);
#     formData.append('teacher_details[number]', event.target.number.value.toString());
#     formData.append('teacher_details[age]', event.target.age.value.toString());
#     formData.append('teacher_details[experience]', event.target.experience.value.toString());
#     formData.append('teacher_details[address]', event.target.address.value.toString());
    

    

#     try {
#       const res = await axios.post(baseURL + '/api/accounts/teacher/teacher_signup/', formData);
#       console.log(formData)
#       if (res.status === 200) {
#         console.log('Server Response:', res.data);
#         console.log('logined');
#         navigate('/teacher/login'); 
#         return res;
#       }
#     } catch (error) {
#       if (error.response && error.response.status === 400) {
#         console.log('Error:', error.response.data);
#         console.log(formData)
#       } else {
#         console.log('Error:', error.message);
#         console.log(formData)
#       }
#     }
#   };

#   return (
#     <div className=" p-6 bg-gray-100 flex items-center justify-center">
#       <div className="container max-w-screen-lg mx-auto my-10">
#         <div>
#           <div className="bg-white rounded shadow-lg p-4 px-4 md:p-8 mb-6">
#             <div className="grid gap-4 gap-y-2 text-sm grid-cols-1 lg:grid-cols-3">
#               <div className="text-gray-600">
#                 <p className="font-medium text-orange-500 text-lg">Personal Details</p>
#                 <p>Please fill out all the fields.</p>
#               </div>
       
#               <div className="lg:col-span-2">
#               <form method='post' onSubmit={handleFormSubmit} encType='multipart/form-data'>
#                 <div className="grid gap-4 gap-y-2 text-sm grid-cols-1 md:grid-cols-6">
#                   <div className="md:col-span-6">
#                     <label htmlFor="username">Full Name</label>
#                     <input type="text" name="username" id="username" placeholder='enter your name' className="h-10 border mt-1 rounded px-4 w-full bg-gray-50"  />
#                   </div>

#                   <div className="md:col-span-6">
#                     <label htmlFor="email">Email Address</label>
#                     <input type="email" name="email" id="email" className="h-10 border mt-1 rounded px-4 w-full bg-gray-50"  placeholder="enetr your email" />
#                   </div>

#                   <div className="md:col-span-3">
#                     <label htmlFor="password">Password</label>
#                     <input type="password" name="password" id="password" className="h-10 border mt-1 rounded px-4 w-full bg-gray-50"  placeholder="enter password" />
#                   </div>

#                   <div className="md:col-span-3">
#                     <label htmlFor="cpassword">Confirm Password</label>
#                     <input type="password" name="cpassword" id="cpassword" className="h-10 border mt-1 rounded px-4 w-full bg-gray-50"  placeholder="confirm password" />
#                   </div>

#                   <div className="md:col-span-2">
#                     <label htmlFor="number">Phone Number</label>
#                     <div className="h-10 bg-gray-50 flex border border-gray-200 rounded items-center mt-1">
#                       <input type='text' name="number" id="number"  placeholder='phone number' className="px-4 appearance-none outline-none text-gray-800 w-full bg-transparent"  />
                      
#                     </div>
#                   </div>

#                   <div className="md:col-span-2">
#                     <label htmlFor="age">Age</label>
#                     <div className="h-10 bg-gray-50 flex border border-gray-200 rounded items-center mt-1">
#                       <input type='text' name="age" id="age" placeholder="age " className="px-4 appearance-none outline-none text-gray-800 w-full bg-transparent"  />
                    
#                     </div>
#                   </div>

#                   <div className="md:col-span-2">
#                     <label htmlFor="experiance">Year of experiance</label>
#                     <div className="h-10 bg-gray-50 flex border border-gray-200 rounded items-center mt-1">
#                       <input type='text' name="experience" id="experiance" placeholder="experiance" className="px-4 appearance-none outline-none text-gray-800 w-full bg-transparent"  />
#                     </div>
#                   </div>

#                   <div className="md:col-span-6">
#                     <label htmlFor="address">Address</label>
#                     <textarea name="address" id="address" className="h-20 border mt-1 rounded px-4 w-full bg-gray-50 resize-none" placeholder="Enter your address"></textarea>
#                 </div>



#                   <div className="md:col-span-2">
#                     <label htmlFor="soda">Upload Documents</label>
#                     <div className="h-10 w-28 bg-gray-50 flex border border-gray-200 rounded items-center mt-1">
#                       <input type='file' name="documents" id="documents" className="px-2 text-center appearance-none outline-none text-gray-800 w-full bg-transparent"  />
#                     </div>
#                   </div>

#                   <div className="md:col-span-5 text-right">
#                     <div className="inline-flex items-end">
#                       <button className="bg-orange-500 hover:bg-orange-700 text-white font-bold py-2 px-4 rounded">Submit</button>
#                     </div>
#                   </div>
#                 </div>
#                 </form>
#               </div>
          


#             </div>
#           </div>
#         </div>
#       </div>
#     </div>
#   );
# };

# export default TeacherSignup;




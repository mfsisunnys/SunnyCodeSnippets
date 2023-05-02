import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import kyc from '../../assets/Images/KYC.png';
import membership from '../../assets/Images/membership-type.png';

import Button from '../UI/Button';

import { getMembership } from '../../apicalls/membership';
import Membership from '../MemberShip/Membership';

const Kyc = () => {
  const navigate = useNavigate();
  const [kycStatus, setKycStatus] = useState(false);
  const [isMember, setIsMember] = useState('');
  useEffect(() => {
    const user = localStorage.getItem('user');
    const token = user ? JSON.parse(user).token : null;
    const kycStatus = user ? JSON.parse(user).kyc_status : false;
    setKycStatus(kycStatus);

    getMembership()
      .then((response) => {
        setIsMember(response.data.data.status);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    <>
      {isMember === 'EXPIRED' || isMember === '' ? (
        <Membership />
      ) : isMember === 'IN PROGRESS' ? (
        <section className="px-7 xl:px-28 2xl:px-28 flex flex-col justify-center items-center w-full transformDiv ">
          <div className="w-full lg:w-3/5">
            <div className="w-full border-2 border-[#4Fb948] rounded-lg flex flex-col gap-8 p-8 my-auto mx-auto xl:w-1/2 2xl:w-2/5">
              <div className="flex flex-row justify-center p-4">
                <img src={membership} alt="kyc" className="h-8  " />
                <span className=" text-2xl">Membership</span>
              </div>
              <hr className="border-1 border-gray-300" />

              <h5 className="text-3xl text-center p-4">
                Your membership purchase is in-progress, please wait for a while
              </h5>
            </div>
          </div>
        </section>
      ) : (
        <section className="px-7 xl:px-28 2xl:px-28 flex flex-col justify-center items-center w-full transformDiv">
          <div className="w-full lg:w-3/5">
            <div className="w-full border-2 border-[#4Fb948] rounded-lg flex flex-col gap-8 p-8 my-auto mx-auto xl:w-1/2 2xl:w-2/5">
              <div className="flex flex-row justify-center p-4">
                <img src={kyc} alt="kyc" className="h-8  " />
                <span className=" text-2xl">KYC/AML</span>
              </div>
              <hr className="border-1 border-gray-300" />
              {kycStatus ? (
                <h5 className="text-xl text-center p-4">
                  Your KYC/AML process is completed. You can now proceed to
                  advance your crypto.
                </h5>
              ) : (
                <>
                  <h5 className="2xl:text-2xl xl:text-3xl sm:text-base text-3xl text-center p-6">
                    Follow the instructions and complete your KYC/AML progress.
                    Your account will not be activated until you have
                    successfully complete the KYC/AML process.
                  </h5>
                  <button
                    onClick={() => navigate('/kyc-aml/sumsub')}
                    className="w-full bg-[#4Fb948] text-white py-3 rounded-md"
                  >
                    {' '}
                    Continue{' '}
                  </button>
                </>
              )}
            </div>

            <div className="box-border w-1/3  row-span-4 p-3 lg:block md:block sm:block hidden"></div>
          </div>
        </section>
      )}
    </>
  );
};
export default Kyc;

import { backendAPI } from './common';

export const kycAccessToken = () => {
  // this function is used to get the access token for the kyc
  return new Promise((resolve, reject) => {
    backendAPI
      .get('/kyc/access-token', {})
      .then((response) => {
        resolve(response);
      })
      .catch((error) => {
        reject(error);
      });
  });
};

export const kycVerify = () => {
  // this function is used to verify the kyc of the user
  return new Promise((resolve, reject) => {
    backendAPI
      .get('/kyc/verify', {})
      .then((response) => {
        resolve(response);
      })
      .catch((error) => {
        reject(error);
      });
  });
};

export const kycDetails = () => {
  // this function is used to get fetch the kyc details of the user
  return new Promise((resolve, reject) => {
    backendAPI
      .get('/kyc', {})
      .then((response) => {
        resolve(response);
      })
      .catch((error) => {
        reject(error);
      });
  });
};

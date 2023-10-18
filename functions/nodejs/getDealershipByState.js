/**
 * Get all dealerships by state
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');

async function main(params) {
    const authenticator = new IamAuthenticator({ apikey: params.CLOUDANT_APIKEY })
    const cloudant = CloudantV1.newInstance({
        authenticator: authenticator
    });
    cloudant.setServiceUrl(params.CLOUDANT_URL);

    try {
        const dbAllDealerships = await cloudant.postFind({
            db: 'dealerships',
            selector: { state: params.STATE },
            fields: ['id', 'city', 'state', 'st', 'address', 'zip', 'lat', 'long']
        });

        return { "dealerships": dbAllDealerships.result.docs };
    } catch (error) {
        if (error.code === 404) {
            return { error: 'The state does not exist' };
        }
        else if (error.code === 500) {
            return { error: 'Something went wrong on the server' };
        }
        else {
            return {
                error: `
            code: ${error.code},
            status: ${error.status},
            statusText: ${error.statusText},
            message: ${error.message},
            cloudant_error: ${error.result.error},
            cloudant_error_reason: ${error.result.reason},
            ` };
        }
    }
}

global.main = main;
/**
 * Get all dealerships
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
        const dealerships = [];
        const dbAllDealerships = await cloudant.postAllDocs({ db: 'dealerships', includeDocs: true });
        dbAllDealerships.result.rows.map(({
            doc: {
                address,
                city,
                full_name,
                id,
                lat,
                long,
                short_name,
                st,
                zip
            }
        }) => {
            dealerships.push({
                address,
                city,
                full_name,
                id,
                lat,
                long,
                short_name,
                st,
                zip
            });
        });

        return { "body": dealerships };
    } catch (error) {
        if (error.code === 404) {
            return { error: 'The database is empty' };
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
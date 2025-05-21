from flask import Flask, jsonify
from flasgger import Swagger, swag_from
from flask_cors import CORS
import subprocess


app = Flask(__name__)
CORS(app)
swagger = Swagger(app)


@app.route('/api/deploy', methods=['POST'])
@swag_from({
    'responses': {
        200: {
            'description': 'Deployment script executed successfully',
            'examples': {
                'application/json': {
                    'success': True,
                    'output': 'Deployment started...'
                }
            }
        },
        500: {
            'description': 'Deployment failed'
        }
    },
    'tags': ['Deployment'],
    'summary': 'Trigger deploy.sh script',
    'description': 'This endpoint runs deploy.sh using subprocess on the server.',
})
def trigger_deploy_script():
    try:
        result = subprocess.run(['bash', '../Sriram/deploy.sh'], capture_output=True, text=True, check=True)

        return jsonify({'success': True, 'output': result.stdout})
    except subprocess.CalledProcessError as e:
        return jsonify({'success': False, 'error': e.stderr}), 500

if __name__ == '__main__':
    app.run(host='localhost', port=3001)

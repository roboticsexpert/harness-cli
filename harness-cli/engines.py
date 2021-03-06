#!/usr/bin/env python3

from harness import EnginesClient, HttpError

from common import *

engine_client = EnginesClient(
    url=url,
    user_id=client_user_id,
    user_secret=client_user_secret
)


if args.action == 'create':
    with open(args.config) as data_file:
        config = json.load(data_file)
        try:
            res = engine_client.create(config)
            print_success(res, 'Created new engine: \n')
        except HttpError as err:
            print_failure(err, 'Error creating new engine\n')

elif args.action == 'update':
    engine_id, config = id_and_config()
    # print("Engine-id: " + engine_id)
    # print("Json config: \n" + str(config))
    try:
        res = engine_client.update(engine_id=engine_id, import_path=args.import_path, update_type="configs", data=config)
        # print_success_string('Updating engine-id: {} \n'.format(engine_id))
        print_success(res, 'Updating engine: \n')
    except HttpError as err:
        print_failure(err, 'Error updating engine-id: {}\n'.format(engine_id))

#    with open(args.config) as data_file:
#        config = json.load(data_file)
#        engine_id = config.engine_id
#        try:
#            res = engine_client.update(config)
#            print_success(res, 'Updating engine: ')
#        except HttpError as err:
#            print_failure(err, 'Error updating engine\n')

#    engine_id, config = id_or_config()
#    try:
#        res = engine_client.update(engine_id, config, args.delete, args.force, args.input)
#        print_success(res, 'Updating existing engine. Success:\n')
#    except HttpError as err:
#        print_failure(err, 'Error updating engine.')

elif args.action == 'import':
    engine_id = args.engine_id
    # print("Import path: {}".format(args.import_path))
    try:
        res = engine_client.update(engine_id=engine_id, import_path=args.import_path, update_type="imports", data={})
        print_success(res, 'Importing to engine: {}\n'.format(engine_id))
    except HttpError as err:
        print_failure(err, 'Error importing to engine-id: {} from {}\n'.format(engine_id, args.import_path))
        #  else:
        #      print_failure(None, "Error: no input for import command.")

elif args.action == 'train':
    engine_id = args.engine_id
    # print("Import path: {}".format(args.import_path))
    try:
        res = engine_client.update(engine_id=engine_id, import_path=args.import_path, update_type="jobs", data={})
        print_success(res, 'Asking engine: {} to train\n'.format(engine_id))
    except HttpError as err:
        print_failure(err, 'Error requesting engine: {} to train\n'.format(engine_id))
        #  else:
        #      print_failure(None, "Error: no input for import command.")

elif args.action == 'delete':
    engine_id, config = id_or_config()
    try:
        res = engine_client.delete(engine_id=engine_id)
        print_success_string('Deleted engine-id: {} \n'.format(engine_id))
    except HttpError as err:
        print_failure(err, 'Error deleting engine-id: {}\n'.format(engine_id))

elif args.action == 'status':
    engine_id = args.engineid
    try:
        if engine_id is not None:
            res = engine_client.get(engine_id=engine_id)
            # print(str(res))
            print_success(res, 'Status for engine-id: {}\n'.format(engine_id))
        else:
            res = engine_client.get(engine_id=None)
            # print(str(res))
            print_success(res, 'Status for all Engines:\n')
    except HttpError as err:
        print_failure(err, 'Error getting status.\n')

elif args.action == 'cancel':
    engine_id = args.engineid
    job_id = args.jobid
    try:
        res = engine_client.cancel_job(engine_id=engine_id, job_id=job_id)
        print_success_string('Cancelled job {}, engine-id: {} \n'.format(job_id, engine_id))
    except HttpError as err:
        print_failure(err, 'Error canceling job {}, engine-id: {}\n'.format(job_id, engine_id))

else:
    print_warning("Unknown action: %{}".format(args.action))

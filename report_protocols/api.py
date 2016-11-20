from tastypie.resources import ModelResource
from tastypie.constants import ALL
from django.conf.urls import url
from tastypie.utils import trailing_slash
import json
from collections import Counter

from report_protocols.models import Workflow, Protocol

class ProtocolResource(ModelResource):
    """allow search in protocol table"""
    class Meta:
        queryset = Workflow.objects.all()
        resource_name = 'protocol'
        filtering = {'name': ALL}
        #allowed_methods = ('get', 'put', 'post', 'delete', 'patch')

class WorkflowResource(ModelResource):
    """allow search in workflow table"""
    class Meta:
        queryset = Workflow.objects.all()
        resource_name = 'workflow'
        filtering = {'project_uuid': ALL}
        #allowed_methods = ('get', 'put', 'post', 'delete', 'patch')

    #agnade al mapeo de urls los webservices que desarrolleis
    def prepend_urls(self):
        return [
            url(r"^(%s)/addOrUpdateWorkflow%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('addOrUpdateWorkflow'), name="api_add_useraddOrUpdateWorkflow"),
            url(r"^(%s)/reportProtocolUsage%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('reportProtocolUsage'), name="reportProtocolUsage"),
        ]

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def addOrUpdateWorkflow(self, request, * args, **kwargs):
        """receive a json dictionary with protocols
           store the dictionary in workflow table
           increase the number of times attribute
           parse dictionary and updates protocol usage in protocol table
           #should you need to debug the following commands may come handy
           curl -i -d "project_uuid=hh&project_workflow=kk" http://localhost:8000/report_protocols/api/workflow/workflow/addOrUpdateWorkflow/
           #curl -i  http://secret-reaches-65198.herokuapp.com/report_protocols/api/workflow/workflow/?project_uuid=ed566c70-3118-4722-86ad-06f1f6e77e74
           curl -i  http://calm-shelf-73264.herokuapp.com/report_protocols/api/workflow/workflow/?project_uuid=ed566c70-3118-4722-86ad-06f1f6e77e74
           curl -i -d "project_uuid=hh&project_workflow=kk" http://calm-shelf-73264.herokuapp.com/report_protocols/api/workflow/workflow/addOrUpdateWorkflow/
                   """
        project_uuid = request.POST['project_uuid']
        project_workflow = request.POST['project_workflow']
        project_workflowCounter = Counter([x.encode('latin-1') for x in json.loads(project_workflow)])

        workflow, created = Workflow.objects.get_or_create(project_uuid=project_uuid)
        if not created:
            dabase_workflowCounter  = Counter([x.encode('latin-1') for x in json.loads(workflow.project_workflow)])
        else:
            dabase_workflowCounter  = Counter([x.encode('latin-1') for x in json.loads(project_workflow)])
        workflow.project_workflow = project_workflow
        workflow.client_ip = self.get_client_ip(request)
        workflow.timesModified += 1
        workflow.save()

        print "project_workflowList", project_workflowCounter
        print "workflow.project_workflow", dabase_workflowCounter
        #if workflow already exists substract before adding
        if not created:
            print "not created"
            project_workflowDict =  project_workflowCounter - dabase_workflowCounter
        else:
            print "created"
            project_workflowDict =project_workflowCounter

        print "project_workflowDict_2", project_workflowDict
        for protocolName, numberTimes in project_workflowDict.iteritems():
            if Protocol.objects.filter(name=protocolName).exists():
                protocolObj = Protocol.objects.get(name=protocolName)
            else:
                protocolObj = Protocol(name=protocolName)
            protocolObj.timesUsed += numberTimes
            protocolObj.save()
        statsDict = {}
        statsDict['error'] = False
        return self.create_response(request, statsDict)

    def deleteObject(self, request):
        project_uuid = request.POST['project_uuid']
        workflows = Workflow.objects.all()
        if workflows.exists():
            workflows[0].delete()
        statsDict = {}
        statsDict['error'] = False
        return self.create_response(request, statsDict)

    def reportProtocolUsage(self, request, * args, **kwargs):
        """ask for a protocol histogram"""
        pass
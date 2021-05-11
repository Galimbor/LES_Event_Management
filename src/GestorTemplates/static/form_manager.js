/**
 * Receives json data from the server, converts it to a javascript object
 * renders the UI according to that data received
 * manipulates the data (create, read, update, delete)
 * sends it back to the server
 * @param {json}   jsonForm         Django form object in json.
 * @param {json}   tiposCampo    Django campo types in json
 * @param {string}   containerDivId Id of the div where the form will be rendered
*/
var FormManager = class {

    /** CONSTRUCT OBJECT Updated**/
    constructor(formularioJson, camposJson, subcamposJson, tiposCampoJson, containerDivId = 'form-wrapper') {
        this.formulario = JSON.parse(formularioJson)[0];
        this.campos = JSON.parse(camposJson);
        this.subcampos = JSON.parse(subcamposJson);
        this.tiposCampo = JSON.parse(tiposCampoJson);
        this.container = $('#' + containerDivId);
        this.activeCampo = null;

        var form = this;
        // collapse campos when clicking outside
        $(window).click(e => form.colapseCampos($('.campos-item')));
    }


    /** RENDER OBJECT **/
    /*
    * Parses json object received from the server to javascrit
    * @param {JSON} rawForm Json form data.
    * @return {object} javascript form object.
    */
    parseJsonForm(rawForm) {
        //The UI already has support for secctions 
        //in case we want to implement them
        var formObj = {
            id: 'form-1',
            title: '',
            description: '',
            campos: []
        }
        formObj.campos = JSON.parse(rawForm);
        return formObj
    }

    isSubcampo(campoObj){
        return (campoObj && campoObj.fields.campo_relacionado!=null)? true : false;
    }

    /* colapse html campos*/
    colapseCampos(items) {
        items.find('.card-header, .campos-config').addClass('is-hidden');
        items.find('input, textarea').not('[disabled]').addClass('is-static');
        items.removeClass('campos-item-active')
    }

    /* expand html campos*/
    expandCampos(questionItems) {
        questionItems.find('.card-header, .campos-config').removeClass('is-hidden');
        questionItems.find('input, textarea').not('[disabled]').removeClass('is-static');
        questionItems.addClass('campos-item-active')
    }

    /*
    * Shows html campo element as active and updates activeCampo variable
    * @param {JQuery Object} htmlQuestionItem
    */
    activateCampo(campo) {
        var todosCampos = $('.campos-item');
        this.colapseCampos(todosCampos);
        this.expandCampos(campo)
        form.activeCampo = form.getCampoById(campo.data('id'));
    }


    setHtmlData(obj, htmlDiv) {

        for (var key in obj.fields) {
            var value = obj.fields[key];
            var objName = obj.model.split('.')[1]
            htmlDiv.find(`.${objName}__${key}`).each(function(){
                var element = $(this);
                if (element.is(':checkbox'))
                    element.prop( "checked", value );
                else if (element.is('input'))
                    element.val(value);
                else if (key == 'position_index')
                    element.html(value + 1);
                else element.html(value);

            })
            
        }
    }

    /*
    * Obtem o template HTML do tipo de campo
    * @param {int} campoId
    */
    getCampoHtml(tipoCampoId){
        var result;
        var tiposCamposHtml = $('.campos-template-wrap').find('.campo-template')
        tiposCamposHtml.each(
            (i, tipocampo ) => ($(tipocampo).data('id') == tipoCampoId) ? result = $(tipocampo) : null
        )
        return result.clone()
    }

    setCampoEventListeners(campoHtml){
        var form = this;

        campoHtml.find('.campos-delete-btn').click(function () {
            form.deleteCampo($(this).data('id'), $(this).data('campo-relacionado'));
        })
        campoHtml.find('.campos-move-up').click(function (e) {
            e.stopPropagation();
            form.moveCampo($(this).data('id'), -1, $(this).data('campo-relacionado'));
        })
        campoHtml.find('.campos-move-down').click(function (e) {
            e.stopPropagation();
            form.moveCampo($(this).data('id'), 1, $(this).data('campo-relacionado'));
        })
        campoHtml.find('.campos-create').click(function (e) {
            e.stopPropagation();
            form.createCampo($(this).data('tipocampoid'), $(this).data('campo-relacionado'));
        })
        campoHtml.find('.campo__conteudo').change(function () {
            form.updateCampo($(this).data('id'), $(this).val(), $(this).data('campo-relacionado'));
        })
        campoHtml.find('.campo__obrigatorio').change(function () {
            var campo = form.getCampoById($(this).data('id'));
            campo.fields.obrigatorio = $(this).is(':checked');
        })
        campoHtml.click(function (e) {
            e.stopPropagation();
            form.activateCampo($(this));
        })
    }

    /*
    * Creates a html element for a campo
    * @param {object} campo
    */
    createCampoHtml(campoObj, isSubcampo=false) {
        var form = this;
        //create element

        var baseTemplateId = isSubcampo? '#subcampo-template-base': '#campo-template-base';
        var campoHtml = $(baseTemplateId).clone();
        campoHtml.find('.campo-content').html(
            this.getCampoHtml(campoObj.fields.tipocampoid)
        );
        
        //pass data id for action buttons and input fields
        campoHtml.find('a, button, input').addBack().attr(
            'data-id',
            campoObj.pk);
        //pass data id for action buttons and input fields
        campoHtml.removeClass('is-hidden');
        campoHtml.attr('id','campo'+campoObj.pk)

        
        if(isSubcampo){
            campoHtml.find('a, button, input').addBack()
                .attr('data-campo-relacionado',campoObj.fields.campo_relacionado)
                .attr('data-tipocampoid',campoObj.fields.tipocampoid)
                .addClass('is-small');
            campoHtml.find('.subcampos').removeClass('subcampos')
        }

        //fill data
        this.setHtmlData(campoObj, campoHtml);

        if (campoObj == this.activeCampo)
            form.activateCampo(campoHtml);
        
        this.setCampoEventListeners(campoHtml);

        return campoHtml;
    }

    /*
    * Renders a campo in the form and updates its position when this parameter is passed
    * @param {string} id of the form.
    * @param {object} campo object.
    * @param {int} (optional) campo index position in the list of campos.
    */
    renderCampo(formDivId, campoObj, campoPosicao = null, focus = false) {
        //update positions
        var form = this;
        if (campoPosicao >= 0)
            campoObj.fields.position_index = campoPosicao;

        var campoHtml = form.createCampoHtml(campoObj);
        var camposContainer = this.container.find(`#${formDivId} .campos`);

        //render subcampos
        var subCamposCount=0;
        self.form.subcampos.forEach(function(subcampo){
            if(subcampo.fields.campo_relacionado==campoObj.pk){
                if(!subCamposCount)
                    campoHtml.find('.subcampos').html('');
                subcampo.fields.position_index = campoPosicao+(subCamposCount+1)/10;
                var subCampoHtml = form.createCampoHtml(subcampo, true);
                campoHtml.find('.subcampos').append(subCampoHtml);
                subCamposCount++;
            }
        })

        camposContainer.append(campoHtml);
    }

    //Updated
    renderFormulario(){
        var formDiv = $('#form-template').clone();
        this.container.append(formDiv);
        formDiv.removeClass('is-hidden');
        formDiv.attr('id', 'form-1');
        this.setHtmlData(this.formulario, $('#gestor-templates-wrapper'))  
        var form = this; 

        //listeners 
        $('.form-header').click(function (e) {
            e.stopPropagation();
            form.expandCampos($(this));
        })
        formDiv.find('.formulario__nome').change(function (e) {
            form.formulario.fields.nome = $(this).val()
            $('.formulario__nome').html($(this).val());
        })
        $('.button.ver_form_config').click(e => $('.modal.ver_form_config').addClass('is-active'))
        $('.button.save-form').click(e => form.saveRemotely())


    }

    /*
    * Renders the entire form
    */
    renderAll() {
        //render form
        this.container.html('');
        this.renderFormulario()
        //render fields
        this.campos.forEach((q, i) => this.renderCampo('form-1', q, i));
    }

    /** MANIPULATE OBJECT **/
    /*
    * Selects a campo by id
    * @param {int} campo id/pk .
    */
    getCampoById(questionId, listaCampos=null) {
        var result;
        var campos = listaCampos? listaCampos: this.campos;
        campos.some(function (q,i) {
            if (q.pk == questionId) {
                result = q;
                result.array_index = i;
                return true;
            }
        });
        return result;
    }

    /*
    * Reorders the position of campos and rerenders the form
    * @param {int} campo id/pk to be repositioned.
    */
    moveCampo(campoID, moveCount, campoRelacionado=null) {
        var campos, campoObj;
        var boundStart, boundEnd;
        if (campoRelacionado){
            campoObj = form.getCampoById(campoID, this.subcampos)
            campos = this.subcampos;
            boundStart=0, boundEnd=campos.length;
        }
        else{
            campoObj = form.getCampoById(campoID, this.campos)
            campos = this.campos
            boundStart=0, boundEnd=campos.length;
        }
        var oldPosition = campoObj.array_index;
        var newPosition = oldPosition + moveCount;
        if (newPosition >= boundStart && newPosition < boundEnd) {
            //remove from old position
            campos.splice(oldPosition, 1);
            //insert at new position
            campos.splice(newPosition, 0, campoObj);
            this.renderAll();
        }
    }


    /*
    * Deletes a campo
    * @param {int} campo id/pk.
    */
    deleteCampo(campoID, campoRelacionado=null) {
        var campos, campoObj;
        if (campoRelacionado){
            campoObj = form.getCampoById(campoID, this.subcampos)
            campos = this.subcampos;
        }
        else{
            campoObj = form.getCampoById(campoID, this.campos)
            campos = this.campos
        }

        if (campoObj) {
            campos.splice(campoObj.array_index, 1);
            this.renderAll();
        }
    }


    /*
    * Creates a campo
    * @param {int} campo type pk.
    */
    createCampo(tipocampo, campoRelacionado=null) {
        var campos;
        if (campoRelacionado){
            campos = this.subcampos;
        }
        else{
            campos = this.campos
        }
        // TODO it should request the server to create a campo
        // this way it will always be in sync with the database
        var campoObj = {
            "model": "forms_manager.campo",
            "pk": campos.length*-1,
            "fields": {
                "conteudo": "",
                "tipocampoid": tipocampo,
                "text_field": "asd",
                "position_index": 1,
                "campo_relacionado": campoRelacionado,
                "form": 6
            }
        }
        campos.push(campoObj);
        this.renderAll();
    }


    /*
    * Creates a campo
    * @param {int} campo id/pk.
    * @param {int} campo id/pk.
    */
    updateCampo(campoID, val, campoRelacionado) {
        var campos, campoObj;
        if (campoRelacionado){
            campoObj = form.getCampoById(campoID, this.subcampos)
            campos = this.subcampos;
        }
        else{
            campoObj = form.getCampoById(campoID, this.campos)
            campos = this.campos
        }
        campoObj.fields.conteudo = val;
    }

    /*
    * Posts form
    */
    saveRemotely() {
        $.ajax({
            contentType: 'application/json; charset=utf-8',
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            data: JSON.stringify(this),
            dataType: 'json',
            success: function(response) {
                console.log(response);
            },
            error: function(response) {
                console.log(response);
                //informar utilizador que nao foi possível guardar no servidor, e a respectiva razão
                //guardar localmente ?
            }
        })
    }
};